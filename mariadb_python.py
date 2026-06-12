import mariadb
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

def get_connection():
    try:
        conn = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mariadb.Error as e:
        print(f"Error: {e}")
        raise RuntimeError(f"DB connection failed: {e}")

def ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            username      VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role          VARCHAR(20) NOT NULL DEFAULT 'user'
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS adjectives (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            adjective VARCHAR(50) UNIQUE NOT NULL,
            counter   INT NOT NULL DEFAULT 1,
            user_id   INT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def create_user(username: str, password_hash: str, role: str = "user") -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return None
    return {"id": row[0], "username": row[1], "password_hash": row[2], "role": row[3]}


def get_adjectives():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT adjective, counter FROM adjectives;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return {adj: count for adj, count in results}


def get_adjectives_admin():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.adjective, a.counter, u.username
        FROM adjectives a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.counter DESC;
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"adjective": adj, "counter": count, "username": username}
        for adj, count, username in results
    ]


def write(word: str, user_id: int = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT counter FROM adjectives WHERE adjective = ?", (word,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE adjectives SET counter = counter + 1 WHERE adjective = ?", (word,))
    else:
        cur.execute(
            "INSERT INTO adjectives (adjective, counter, user_id) VALUES (?, 1, ?)",
            (word, user_id)
        )
    conn.commit()
    cur.close()
    conn.close()


def delete_adjective(word: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM adjectives WHERE adjective = ?", (word,))
    conn.commit()
    cur.close()
    conn.close()
