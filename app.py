from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

DB_PATH = "orders.db"

# تهيئة قاعدة البيانات لو مش موجودة
def init_db():
    need_create = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if need_create:
        c.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                color TEXT,
                payment TEXT,
                quantity INTEGER,
                created_at TEXT
            )
        """)
        conn.commit()
    conn.close()

init_db()

# الصفحة الرئيسية
@app.route("/")
def index():
    return render_template("index.html")

# صفحة الطلب
@app.route("/order", endpoint="order")
def order_page():
    return render_template("order.html")

# استلام الطلب من الفورم وحفظه في SQLite
@app.route("/submit_order", methods=["POST"])
def submit_order():
    # أخذ القيم من الفورم
    product = request.form.get("selectedProduct", "")
    name = request.form.get("fullName", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    address = request.form.get("address", "")
    color = request.form.get("color", "")
    payment = request.form.get("paymentMethod", "")
    quantity = request.form.get("quantity", 1)

    # حفظ في قاعدة البيانات
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders (product, name, email, phone, address, color, payment, quantity, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (product, name, email, phone, address, color, payment, int(quantity), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

    # حفظ الطلب في الجلسة للسلة
    session['last_order'] = {
        "product": product,
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "color": color,
        "payment": payment,
        "quantity": quantity
    }

    # إعادة التوجيه لصفحة السلة/تأكيد الطلب
    return redirect(url_for("cart"))

# صفحة سلة المشتريات
@app.route("/cart")
def cart():
    last_order = session.get("last_order")
    return render_template("cart.html", order=last_order)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

