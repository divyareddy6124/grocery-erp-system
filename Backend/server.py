from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ---------------- DB CONNECTION ----------------

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="grocery_store",
        ssl_disabled=True
    )

# ---------------- HOME ----------------

@app.route('/')
def home():
    return "ERP Backend Running 🚀"

# ---------------- PRODUCTS ----------------

@app.route('/getProducts', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.product_id,
            p.name,
            u.uom_name,
            p.price_per_unit
        FROM products p
        JOIN uom u ON p.uom_id = u.uom_id
    """)

    data = cursor.fetchall()
    conn.close()
    return jsonify(data)


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)",
        (data['name'], data['uom_id'], data['price'])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Product added"})


@app.route('/deleteProduct/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE product_id=%s", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})

# ---------------- ORDERS ----------------

@app.route('/createOrder', methods=['POST'])
def create_order():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convert to int (important)
    product_id = int(data['product_id'])
    quantity = int(data['quantity'])

    # Get price
    cursor.execute(
        "SELECT price_per_unit FROM products WHERE product_id=%s",
        (product_id,)
    )
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    price = result[0]
    total = price * quantity

    # Insert into correct columns (qty ✅)
    cursor.execute(
        "INSERT INTO orders_new (product_id, qty, total) VALUES (%s, %s, %s)",
        (product_id, quantity, total)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Order created", "total": total})


@app.route('/getOrders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.order_id, 
            p.name, 
            o.qty AS quantity, 
            o.total
        FROM orders_new o
        JOIN products p ON o.product_id = p.product_id
    """)

    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# ---------------- ANALYTICS ----------------

@app.route('/analytics', methods=['GET'])
def analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders_new")
    orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM orders_new")
    revenue = cursor.fetchone()[0] or 0

    conn.close()

    return jsonify({
        "products": products,
        "orders": orders,
        "revenue": revenue
    })

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)