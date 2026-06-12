from flask import Flask, render_template, request, redirect, url_for, flash, session
from mariadb_python import get_adjectives, get_adjectives_admin, write, create_user, get_user, delete_adjective
from wordcloud_python import make_cloud
from hashing import hash_password, check_password
import markdown
import spacy
import time
from pathlib import Path

app = Flask(__name__)
app.secret_key = "test"

nlp = spacy.load("en_core_web_sm")

def _is_adjective(word):
        
    sentences = [
        f"This website is so {word}.",
        f"{word}, that is good",
        f"It was very {word}.",
    ]
    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc:
            if token.text == word:
                if token.pos_ in ("ADJ", "ADV"):
                    return True
    return False

_DOCS_DIR = Path(__file__).parent / "documents"

def _load_doc(filename):
    return markdown.markdown(_DOCS_DIR.joinpath(filename).read_text(encoding="utf-8"), extensions=["extra"])

@app.route("/", methods=["GET"])
def index():
    adjectives = get_adjectives()
    has_cloud = make_cloud(adjectives) != "NOPE"
    wordcloud = {
        "light": url_for("static", filename="images/cloud_light.png"),
        "dark":  url_for("static", filename="images/cloud_dark.png"),
        "ts":    int(time.time()),
    } if has_cloud else None
    return render_template(
        "index.html",
        wordcloud=wordcloud,
        privacy_html=_load_doc("privacy_policy.md"),
        terms_html=_load_doc("terms_of_use.md"),
        manual_html=_load_doc("user_manual.md"),
    )

@app.route("/", methods=["POST"])
def add():
    word = request.form.get("word", "").strip().lower()

    if len(word) <= 3:
        flash(f'"{word}" doesn\'t look like an adjective!', "error")
        return redirect(url_for("index"))
    
    if _is_adjective(word) == True:
        write(word, session.get("user_id"))
        flash(f'"{word}" added!', "success")
        return redirect(url_for("index"))

    if not word:
        flash("Empty input!", "error")
        return redirect(url_for("index"))

    if not _is_adjective(word):
        flash(f'"{word}" doesn\'t look like an adjective!', "error")
        return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        flash("Username and password required.", "error")
        return redirect(url_for("signup"))
    if get_user(username):
        flash("Username already taken.", "error")
        return redirect(url_for("signup"))
    create_user(username, hash_password(password))
    flash("Account created! Please log in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = get_user(username)
    if not user or not check_password(password, user["password_hash"]):
        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        flash("Admin access required.", "error")
        return redirect(url_for("index"))
    adjectives = get_adjectives_admin()
    return render_template("admin.html", adjectives=adjectives)


@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    if session.get("role") != "admin":
        flash("Admin access required.", "error")
        return redirect(url_for("index"))
    word = request.form.get("word", "")
    if word:
        delete_adjective(word)
        flash(f'"{word}" deleted.', "success")
    return redirect(url_for("admin"))




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
 