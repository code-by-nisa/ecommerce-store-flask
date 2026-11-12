from flask import Flask, render_template, session, redirect, url_for, request, abort

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # Replace with a private random key before production.

CATEGORIES = [
    "Fashion",
    "Bags",
    "Accessories",
    "Home Decor",
    "Electronics",
    "Beauty",
]

# Starter catalog: replace names, photos, descriptions and prices with your actual inventory.
PRODUCTS = [
    {"id": 1, "name": "Linen Tailored Shirt", "category": "Fashion", "price": 48, "desc": "An effortless wardrobe staple in breathable, refined linen.", "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=900"},
    {"id": 2, "name": "Everyday Knit Set", "category": "Fashion", "price": 76, "desc": "A soft, versatile set designed for relaxed elegance.", "image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=900"},
    {"id": 3, "name": "Classic Evening Dress", "category": "Fashion", "price": 112, "desc": "A timeless silhouette for dinners, celebrations and special moments.", "image": "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=900"},
    {"id": 4, "name": "Structured Everyday Tote", "category": "Bags", "price": 89, "desc": "A spacious, structured carryall for workdays and weekends.", "image": "https://images.unsplash.com/photo-154 handbag?w=900"},
    {"id": 5, "name": "Minimal Shoulder Bag", "category": "Bags", "price": 95, "desc": "A polished everyday bag with a clean, minimal profile.", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=900"},
    {"id": 6, "name": "Weekend Travel Holdall", "category": "Bags", "price": 128, "desc": "A roomy companion for short escapes and overnight stays.", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=900"},
    {"id": 7, "name": "Sculpted Gold Earrings", "category": "Accessories", "price": 38, "desc": "A subtle statement pair with a warm gold finish.", "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=900"},
    {"id": 8, "name": "Everyday Leather Wallet", "category": "Accessories", "price": 52, "desc": "A slim essential with thoughtful space for daily cards.", "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=900"},
    {"id": 9, "name": "Classic Dial Watch", "category": "Accessories", "price": 145, "desc": "A refined timepiece with a clean, understated face.", "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=900"},
    {"id": 10, "name": "Ceramic Table Vase", "category": "Home Decor", "price": 42, "desc": "A sculptural accent for shelves, consoles and dining tables.", "image": "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=900"},
    {"id": 11, "name": "Soft Neutral Cushion", "category": "Home Decor", "price": 34, "desc": "An inviting texture that brings warmth to your living space.", "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=900"},
    {"id": 12, "name": "Minimal Desk Lamp", "category": "Home Decor", "price": 68, "desc": "Warm, considered lighting for a calm reading corner.", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=900"},
    {"id": 13, "name": "Wireless Earbuds", "category": "Electronics", "price": 79, "desc": "Compact everyday audio for calls, commutes and playlists.", "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=900"},
    {"id": 14, "name": "Portable Bluetooth Speaker", "category": "Electronics", "price": 64, "desc": "Bring clear, convenient sound to your everyday spaces.", "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=900"},
    {"id": 15, "name": "Wireless Charging Stand", "category": "Electronics", "price": 39, "desc": "A tidy charging solution for your bedside or workspace.", "image": "https://images.unsplash.com/photo-1615526675159-e248c3021d3f?w=900"},
    {"id": 16, "name": "Daily Glow Skincare Set", "category": "Beauty", "price": 58, "desc": "A simple self-care set for a fresh, comfortable routine.", "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=900"},
    {"id": 17, "name": "Signature Fragrance", "category": "Beauty", "price": 86, "desc": "A sophisticated scent for day-to-evening wear.", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=900"},
    {"id": 18, "name": "Makeup Brush Collection", "category": "Beauty", "price": 32, "desc": "A curated set of soft brushes for everyday makeup.", "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=900"},
]


def get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)


def cart_items():
    cart = session.get("cart", {})
    items, total = [], 0
    for pid, qty in cart.items():
        p = get_product(int(pid))
        if p:
            subtotal = p["price"] * qty
            total += subtotal
            items.append({"product": p, "qty": qty, "sub": subtotal})
    return items, total


@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(session.get("cart", {}).values()), "categories": CATEGORIES}


@app.route("/")
def home():
    return render_template("home.html", products=PRODUCTS[:6])


@app.route("/shop")
def shop():
    selected_category = request.args.get("category", "").strip()
    products = [p for p in PRODUCTS if not selected_category or p["category"] == selected_category]
    return render_template("shop.html", products=products, selected_category=selected_category)


@app.route("/product/<int:pid>")
def product(pid):
    p = get_product(pid)
    if not p:
        abort(404)
    return render_template("product.html", p=p)


@app.route("/add/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    if not get_product(pid):
        abort(404)
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/remove/<int:pid>", methods=["POST"])
def remove(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        return redirect(url_for("shop"))
    if request.method == "POST":
        order = {k: request.form.get(k, "").strip() for k in ("name", "email", "phone", "address")}
        print("NEW ORDER:", order, items, total)
        session["cart"] = {}
        return render_template("thanks.html", name=order["name"])
    return render_template("checkout.html", items=items, total=total)


if __name__ == "__main__":
    app.run(debug=True)
