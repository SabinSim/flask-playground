from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# The secret key is required for session security
app.secret_key = "super_secret_key"

# Decorator to ensure a user is logged in before accessing a route
def login_required(func):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    # Important: set the wrapper name for Flask compatibility
    wrapper.__name__ = func.__name__ 
    return wrapper

# ---------- Database Initialization Function ----------
def init_db():
    # Connect to the SQLite database file for user storage
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # Create the 'users' table if it doesn't already exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Run database initialization on application start
init_db()

# ---------- User Signup Route ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Hash the password for secure storage
        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        try:
            # Attempt to insert the new user
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_pw)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Handle case where username already exists
            return "Signup failed: Username already exists."
        finally:
            conn.close()

        # Redirect to login page upon successful signup
        return redirect("/login")

    # Render the signup form for GET requests
    return render_template("signup.html")


# ---------- User Login Route ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        # Find the user by username
        cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        # Check if user exists and if the provided password matches the stored hash
        if user and check_password_hash(user[2], password):
            # Set session variables on successful login
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")
        else:
            # Authentication failed
            return "Login failed: Invalid username or password."

    # Render the login form for GET requests
    return render_template("login.html")


# ---------- Dashboard (Logged-in screen) Route ----------
@app.route("/dashboard")
@login_required # Requires user to be logged in
def dashboard():
    # Display a personalized welcome message
    return f"Welcome, {session['username']}! (Dashboard Page)"

# ---------- Logout Route ----------
@app.route("/logout")
def logout():
    # Clear the entire session data
    session.clear() 
    # Redirect to the login page
    return redirect("/login")

# ---------- Home Route ----------
@app.route("/")
def home():
    # Render the main home page
    return render_template("home.html")


if __name__ == "__main__":
    # Run the application
    app.run(debug=True)
