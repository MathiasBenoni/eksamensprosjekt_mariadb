import mariadb
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mariadb.Error as e:
        print(f"Error: {e}")
        sys.exit(1)

def get_adjectives():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT adjective, counter FROM adjectives;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return {adj: count for adj, count in results}

def write(word):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT counter FROM adjectives WHERE adjective = ?", (word,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE adjectives SET counter = counter + 1 WHERE adjective = ?", (word,))
    else:
        cur.execute("INSERT INTO adjectives (adjective, counter) VALUES (?, 1)", (word,))
    conn.commit()
    cur.close()
    conn.close()
