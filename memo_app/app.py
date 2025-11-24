from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------- Database Initialization ----------
def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect("memo.db")
    cur = conn.cursor()
    # Create the 'memos' table if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS memos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Memo List Page (Home) ----------
@app.route("/")
def index():
    # Fetch all memos, ordered by ID (most recent first)
    conn = sqlite3.connect("memo.db")
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM memos ORDER BY id DESC")
    memos = cur.fetchall()
    conn.close()

    return render_template("index.html", memos=memos)

# ---------- Create New Memo Page ----------
@app.route("/new")
def new_memo():
    return render_template("new.html")

# ---------- Save Memo (POST request handler) ----------
@app.route("/create", methods=["POST"])
def create_memo():
    content = request.form["content"]
    # Generate timestamp for creation
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert the new memo into the database
    conn = sqlite3.connect("memo.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO memos (content, created_at) VALUES (?, ?)",
        (content, created_at)
    )
    conn.commit()
    conn.close()

    # Redirect to the home page after saving
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
