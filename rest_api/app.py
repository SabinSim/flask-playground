from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ---------- DB Initialization ----------
def init_db():
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- GET: Retrieve all items ----------
@app.route("/items", methods=["GET"])
def get_items():
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM items")
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({"id": r[0], "name": r[1], "price": r[2]})

    return jsonify(items)

# ---------- GET: Retrieve specific item ----------
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM items WHERE id = ?", (item_id,))
    r = cur.fetchone()
    conn.close()

    if r:
        return jsonify({"id": r[0], "name": r[1], "price": r[2]})
    else:
        return jsonify({"error": "Item not found"}), 404

# ---------- POST: Create item ----------
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({"message": "Created", "id": new_id}), 201

# ---------- PUT: Update item ----------
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (name, price, item_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})

# ---------- DELETE: Delete item ----------
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
