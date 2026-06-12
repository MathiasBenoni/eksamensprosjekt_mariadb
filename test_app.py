import pytest
from unittest.mock import MagicMock, patch
import app as flask_app
import mariadb_python


# --- FIXTURE ---
# @pytest.fixture = reusable setup. Any test that has "client" as parameter gets this automatically.
@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True       # puts Flask in test mode (better error messages)
    flask_app.app.config["WTF_CSRF_ENABLED"] = False
    with flask_app.app.test_client() as c:
        yield c   # "give test the client, then clean up after test finishes"


# ============================================================
# Tests for mariadb_python.py
# All DB calls are mocked — no real MariaDB needed
# ============================================================

class TestGetAdjectives:

    def test_returns_dict(self):
        # MagicMock() = fake DB connection that accepts any method call without crashing
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value  # fake cursor (what conn.cursor() returns)

        # Tell the fake cursor what to return when fetchall() is called
        mock_cur.fetchall.return_value = [("happy", 3), ("sad", 1)]

        # Set the structure of the fake DB to the structure of the real one
        with patch("mariadb_python.get_connection", return_value=mock_conn):
            result = mariadb_python.get_adjectives()

        # Verify the function converted the list of tuples into a dict correctly
        assert result == {"happy": 3, "sad": 1}

    def test_empty_table(self):
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.fetchall.return_value = []  # DB returns nothing

        with patch("mariadb_python.get_connection", return_value=mock_conn):
            result = mariadb_python.get_adjectives()

        assert result == {}  # should return empty dict, not crash

    def test_closes_connection(self):
        # Verify the function always cleans up (closes cursor AND connection)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.fetchall.return_value = []

        with patch("mariadb_python.get_connection", return_value=mock_conn):
            mariadb_python.get_adjectives()

        # Mocks record every call made to them — assert_called_once() checks it happened exactly once
        mock_conn.close.assert_called_once()
        mock_conn.cursor.return_value.close.assert_called_once()


class TestWrite:

    def test_inserts_word(self):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value

        # Simulate word not existing yet — SELECT returns nothing, so the INSERT branch is taken
        # Without this, MagicMock returns a truthy MagicMock for fetchone(), which would
        # make write() take the UPDATE branch and call execute() twice, failing the test
        mock_cur.fetchone.return_value = None

        with patch("mariadb_python.get_connection", return_value=mock_conn):
            mariadb_python.write("brave")

        # Verify execute() was called twice (SELECT check + INSERT) and the INSERT looks correct
        assert mock_cur.execute.call_count == 2
        call_args = mock_cur.execute.call_args   # call_args returns the last call (the INSERT)
        assert "INSERT INTO adjectives" in call_args[0][0]  # [0][0] = first positional arg (the SQL string)
        assert call_args[0][1] == ("brave",)                # [0][1] = second positional arg (the values tuple)

    def test_increments_existing_word(self):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value

        # Simulate word already existing — SELECT returns a row, so the UPDATE branch is taken
        mock_cur.fetchone.return_value = (1,)

        with patch("mariadb_python.get_connection", return_value=mock_conn):
            mariadb_python.write("brave")

        # execute() is called twice here (SELECT then UPDATE) — check the last call is the UPDATE
        call_args_list = mock_cur.execute.call_args_list
        last_call = call_args_list[-1]
        assert "UPDATE adjectives" in last_call[0][0]
        assert last_call[0][1] == ("brave",)

    def test_commits(self):
        # If commit() is never called, data is lost — verify it always happens
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.fetchone.return_value = None  # take the INSERT branch

        with patch("mariadb_python.get_connection", return_value=mock_conn):
            mariadb_python.write("brave")

        mock_conn.commit.assert_called_once()

    def test_closes_connection(self):
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.fetchone.return_value = None  # take the INSERT branch

        with patch("mariadb_python.get_connection", return_value=mock_conn):
            mariadb_python.write("brave")

        mock_conn.close.assert_called_once()
        mock_conn.cursor.return_value.close.assert_called_once()


# ============================================================
# Tests for Flask routes in app.py
# Uses the "client" fixture defined at the top
# ============================================================

class TestIndexRoute:

    def test_get_status_200(self, client):
        # patch get_adjectives so the route never calls the real DB
        with patch("app.get_adjectives", return_value={"happy": 2}):
            response = client.get("/")
        assert response.status_code == 200  # 200 = OK

    def test_renders_adjectives(self, client):
        with patch("app.get_adjectives", return_value={"happy": 2, "sad": 1}):
            response = client.get("/")
        assert response.status_code == 200
        assert b"cloud_light.png" in response.data
        assert b"cloud_dark.png" in response.data

    def test_empty_adjectives(self, client):
        # Should not crash when DB is empty
        with patch("app.get_adjectives", return_value={}):
            response = client.get("/")
        assert response.status_code == 200


class TestAddRoute:

    def test_valid_word_redirects(self, client):
        # patch("app.write") replaces write() with a fake so no DB call happens
        # "as mock_write" gives us a reference so we can inspect calls later
        with patch("app.write") as mock_write:
            response = client.post("/", data={"word": "brave"})
        assert response.status_code == 302          # 302 = redirect (expected after POST)
        mock_write.assert_called_once_with("brave") # verify write() was called with correct word

    def test_strips_and_lowercases(self, client):
        # app.py does .strip().lower() — verify "  BRAVE  " becomes "brave"
        with patch("app.write") as mock_write:
            client.post("/", data={"word": "  BRAVE  "})
        mock_write.assert_called_once_with("brave")

    def test_empty_word_no_write(self, client):
        # Empty string should be rejected — write() must NOT be called
        with patch("app.write") as mock_write:
            response = client.post("/", data={"word": ""})
        mock_write.assert_not_called()  # assert_not_called() = crash if write() was called
        assert response.status_code == 302  # still redirects, but with error flash

    def test_whitespace_only_no_write(self, client):
        # "   " after .strip() becomes "" — should also be rejected
        with patch("app.write") as mock_write:
            client.post("/", data={"word": "   "})
        mock_write.assert_not_called()

    def test_missing_word_field_no_write(self, client):
        # Form submitted with no "word" field at all — should not crash or write
        with patch("app.write") as mock_write:
            client.post("/", data={})
        mock_write.assert_not_called()