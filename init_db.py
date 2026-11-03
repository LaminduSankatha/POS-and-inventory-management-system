"""
Creates the local SQLite database, default settings, user accounts, sample categories
and sample products (with generated SVG placeholder images).

Usage:   python init_db.py          (safe: does nothing if data already exists)
         python init_db.py --reset  (DELETES everything and starts fresh)
"""
import sys
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models import User, Category, Product, Setting, DEFAULT_SETTINGS
from app.utils import now_local

SAMPLE_CATEGORIES = ["Grocery", "Drinks", "Dairy", "Bakery", "Snacks",
                     "Household", "Personal Care", "Frozen Food"]

# (name, category, selling, buying_or_None, stock, min_stock, quick_sale)
SAMPLE_PRODUCTS = [
    ("Milk Powder 400g",              "Dairy",         690,  590,  24,  6, True),
    ("Milk Powder 1kg",               "Dairy",        1650, 1420,  10,  4, False),
    ("Fresh Milk 1L",                 "Dairy",         380,  330,  30, 10, True),
    ("Chocolate Milk 200ml",          "Dairy",         120,   95,   0, 12, False),  # out of stock demo
    ("Buffalo Curd 500g",             "Dairy",         320,  260,   8,  4, False),
    ("Eggs (Pack of 10)",             "Dairy",         450,  390,   5,  6, True),   # low stock demo
    ("Coca Cola 1L",                  "Drinks",        420,  360,  25,  6, True),
    ("Ginger Beer 1L",                "Drinks",        380,  320,  18,  6, False),
    ("Drinking Water 500ml",          "Drinks",         60,   45,  72, 24, True),
    ("Orange Juice 1L",               "Drinks",        520,  450,   3,  5, False),  # low stock demo
    ("Sliced Bread",                  "Bakery",        190,  160,  12,  5, True),
    ("Buns (Pack of 4)",              "Bakery",        140,  115,  20,  6, False),
    ("White Rice 5kg",                "Grocery",      1450, 1280,  15,  5, True),
    ("Red Raw Rice 5kg",              "Grocery",      1380, 1220,   9,  5, False),
    ("Dhal 1kg",                      "Grocery",       520,  455,  22,  8, True),
    ("White Sugar 1kg",               "Grocery",       290,  250,  26, 10, True),
    ("Wheat Flour 1kg",               "Grocery",       260,  225,  16,  8, False),
    ("Coconut Oil 400ml",             "Grocery",       560,  490,  11,  5, False),
    ("Tea Leaves 200g",               "Grocery",       480,  410,  14,  6, False),
    ("Potato Chips 80g",              "Snacks",         90,   72,  40, 12, False),
    ("Marie Biscuits 200g",           "Snacks",        150,  125,  28, 10, False),
    ("Instant Noodles",               "Snacks",        230,  195,  30, 10, False),
    ("Chocolate Biscuit Roll",        "Snacks",        180,  150,   7,  8, False),  # low stock demo
    ("Soap 100g",                     "Personal Care", 190,  150,  24,  8, False),
    ("Shampoo 200ml",                 "Personal Care", 640,  540,  10,  4, False),
    ("Toothpaste 100g",               "Personal Care", 280,  230,  12,  5, False),
    ("Washing Powder 1kg",            "Household",     890,  760,   8,  5, False),
    ("Dish Wash Liquid 500ml",        "Household",     420,  350,   6,  6, False),  # low stock demo
    ("Frozen Chicken 1kg",            "Frozen Food",  1450, None,   6,  4, False),  # no buying price demo
    ("Ice Cream 1L",                  "Frozen Food",   990,  840,   4,  5, False),  # low stock demo
]

PALETTE = ["#0e7a5f", "#b4632c", "#3f6db5", "#8a3fb5",
           "#b53f5c", "#2c8ab5", "#5c8a2c", "#a06a1f"]


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_svg(name, color):
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    label = _esc(name[:20])
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">'
        f'<rect width="240" height="240" rx="20" fill="{color}"/>'
        '<text x="120" y="118" font-family="Segoe UI, Arial" font-size="72" font-weight="bold" '
        f'fill="#ffffff" text-anchor="middle">{_esc(initials)}</text>'
        '<text x="120" y="165" font-family="Segoe UI, Arial" font-size="19" '
        f'fill="#ffffff" text-anchor="middle">{label}</text></svg>'
    )


def main():
    app = create_app()
    with app.app_context():
        if "--reset" in sys.argv:
            db.drop_all()
            print("Old database removed.")
        db.create_all()
        if User.query.count() > 0:
            print("Database already initialised - nothing was changed.")
            print("(Use  python init_db.py --reset  to start over. WARNING: deletes all data.)")
            return

        for key, value in DEFAULT_SETTINGS.items():
            db.session.add(Setting(key=key, value=value))

        admin = User(username="admin", full_name="Store Owner", role="admin")
        admin.set_password("admin123")
        cashier = User(username="cashier", full_name="Cashier", role="cashier")
        cashier.set_password("cashier123")
        db.session.add_all([admin, cashier])

        cats = {}
        for name in SAMPLE_CATEGORIES:
            c = Category(name=name)
            db.session.add(c)
            cats[name] = c
        db.session.flush()

        upload_dir = Path(app.config["UPLOAD_FOLDER"])
        upload_dir.mkdir(parents=True, exist_ok=True)
        for i, (name, cat, sell, buy, stock, mins, quick) in enumerate(SAMPLE_PRODUCTS):
            fname = f"sample_{i + 1:02d}.svg"
            (upload_dir / fname).write_text(make_svg(name, PALETTE[i % len(PALETTE)]),
                                            encoding="utf-8")
            db.session.add(Product(name=name, category=cats[cat], selling_price=sell,
                                   buying_price=buy, stock=stock, min_stock=mins,
                                   image=fname, is_quick_sale=quick))
        db.session.commit()

        print(f"[OK] Database created: {app.config['DATABASE_FILE']}")
        print(f"[OK] {len(SAMPLE_PRODUCTS)} sample products with images in {upload_dir}")
        print("[OK] Logins ->  admin / admin123   (Administrator)")
        print("                cashier / cashier123 (Cashier)")
        print("     Please change these passwords in Settings.")


if __name__ == "__main__":
    main()