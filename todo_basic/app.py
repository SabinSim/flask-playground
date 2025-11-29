from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

conn = sqlite3.connect("todo.db")  # Connect to database
cur = conn.cursor()  # Cursor (Prepare)
# Execute setup
cur.execute("""   
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER DEFAULT 0,
    created_at TEXT
)
""")   # This is SQL (Database Language)

conn.commit()  # Commit (Confirm/Save)
conn.close()  # Close (End)

print("DB Initialization Complete!")


app = Flask(__name__)

# DB Connection Function
def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    todos = conn.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db()
    conn.execute(
        "INSERT INTO todos (title, created_at) VALUES (?, ?)",
        (title, created_at)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/done/<int:id>")
def done(id):
    conn = get_db()
    conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
