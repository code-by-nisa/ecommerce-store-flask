from flask import Flask, render_template, session, redirect, url_for, request, abort

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # deploy se pehle isay badal dein

# Products yahan edit karein (baad mein hum inhein database mein shift karenge)
PRODUCTS = [
    {"id": 1, "name": "Canvas Tote Bag", "price": 1800, "desc": "Strong cotton canvas, daily use ke liye."},
    {"id": 2, "name": "Leather Wallet", "price": 2500, "desc": "Slim design, 6 card slots."},
    {"id": 3, "name": "Steel Water Bottle", "price": 1500, "desc": "750ml, 12 ghante thanda/garam."},
    {"id": 4, "name": "Desk Organizer", "price": 2200, "desc": "Wooden organizer, pens aur phone stand."},
    {"id": 5, "name": "Notebook Set", "price": 900, "desc": "3 notebooks, dotted pages."},
    {"id": 6, "name": "Wireless Earbuds", "price": 4500, "desc": "Bluetooth 5.3, charging case ke sath."},
]


def get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)


def cart_items():
    cart = session.get("cart", {})
    items, total = [], 0
    for pid, qty in cart.items():
        p = get_product(int(pid))
        if p:
            sub = p["price"] * qty
            total += sub
            items.append({"product": p, "qty": qty, "sub": sub})
    return items, total


@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(session.get("cart", {}).values())}


@app.route("/")
def home():
    return render_template("home.html", products=PRODUCTS[:3])


@app.route("/shop")
def shop():
    return render_template("shop.html", products=PRODUCTS)


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
        order = {k: request.form.get(k, "") for k in ("name", "phone", "address")}
        print("NEW ORDER:", order, items, total)  # abhi sirf terminal mein dikhega
        session["cart"] = {}
        return render_template("thanks.html", name=order["name"])
    return render_template("checkout.html", items=items, total=total)


if __name__ == "__main__":
    app.run(debug=True)
