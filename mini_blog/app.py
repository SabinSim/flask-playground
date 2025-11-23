from flask import Flask, render_template, request, redirect
import sqlite3

# Initialize the Flask application
app = Flask(__name__)

# ---------- Database Initialization Function ----------
def init_db():
    # Connect to the SQLite database file
    conn = sqlite3.connect("blog.db")
    cur = conn.cursor()
    
    # Create the 'posts' table if it doesn't already exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Run database initialization on application start
init_db()

# ---------- Home Route: Display Post List ----------
@app.route("/")
def index():
    # Connect to the database and fetch all posts
    conn = sqlite3.connect("blog.db")
    cur = conn.cursor()
    # Select ID, title, and content, ordering by ID descending (most recent first)
    cur.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = cur.fetchall()
    conn.close()
    
    # Render the index template, passing the list of posts
    return render_template("index.html", posts=posts)

# ---------- New Post Page Route ----------
@app.route("/new")
def new_post():
    # Render the form page for writing a new post
    return render_template("new.html")

# ---------- Post Creation and Storage Route (POST handler) ----------
@app.route("/create", methods=["POST"])
def create_post():
    # Retrieve title and content from the submitted form data
    title = request.form["title"]
    content = request.form["content"]

    # Insert the new post into the database
    conn = sqlite3.connect("blog.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (title, content)
    )
    conn.commit()
    conn.close()

    # Redirect the user to the home page to see the new post
    return redirect("/")

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True)
