"""
reset_data.py - Safe reset tool for the Grocery POS.
Start this with reset_data.bat (double-click the BAT, not this file).
A backup is ALWAYS saved into 'backups' before anything is changed.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

DB_FILE = ROOT / "database" / "grocery.db"
BACKUP_DIR = ROOT / "backups"


def make_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    name = "grocery_backup_before_reset_%s.db" % datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / name
    src = sqlite3.connect(str(DB_FILE))
    dst = sqlite3.connect(str(dest))
    with dst:
        src.backup(dst)
    dst.close()
    src.close()
    return name


def show_counts(title):
    from app.models import (Product, Category, Sale, SaleItem,
                            StockMovement, User)
    counts = {
        "products": Product.query.count(),
        "categories": Category.query.count(),
        "bills": Sale.query.count(),
        "bill lines": SaleItem.query.count(),
        "stock records": StockMovement.query.count(),
        "users": User.query.count(),
    }
    print(title)
    for k, v in counts.items():
        print(f"   {k:14s}: {v}")


def main():
    print("=" * 62)
    print("  RESET TOOL - Disodi Stores POS")
    print("=" * 62)

    if not DB_FILE.exists():
        print("\nNo database found at:", DB_FILE)
        print("Start the app once with run.bat first.")
        return

    print("\nThis tool can reset your data. A BACKUP is saved automatically")
    print("before anything is changed (look in the 'backups' folder).\n")
    print("  1  Delete ALL products and categories")
    print("       Keeps: bills & sales history, users, store name, settings.")
    print("  2  Delete products, categories AND all bills / sales history")
    print("       The fresh start for real trading. Keeps: users, settings.")
    print("  3  FULL factory reset")
    print("       Everything wiped; logins back to admin/admin123 and")
    print("       cashier/cashier123; settings back to defaults.")
    print("  4  Delete ONLY the sales history (bills)")
    print("       Keeps: products, categories, current stock, photos,")
    print("       users, store name, settings. For clearing test bills")
    print("       before going live without touching your product list.")
    print("  5  Cancel - change nothing")

    choice = input("\nType 1, 2, 3, 4 or 5 and press Enter: ").strip()
    if choice not in ("1", "2", "3", "4"):
        print("\nNothing was changed.")
        return

    print("\nYou must close the black POS window (run.bat) before continuing!")
    ready = input("Is the POS window closed? Type YES to continue: ").strip()
    if ready.upper() != "YES":
        print("\nNothing was changed.")
        return

    backup_name = make_backup()
    print(f"\nBackup saved: backups\\{backup_name}")

    from app import create_app
    from app.extensions import db
    from app.models import (Product, Category, Sale, SaleItem, StockMovement,
                            HeldBill, User, Setting, DEFAULT_SETTINGS)

    app = create_app()
    with app.app_context():
        show_counts("\nBEFORE - what is in the database now:")
        print()

        if choice == "1":
            for label, q in (("stock history", StockMovement.query),
                             ("held bills", HeldBill.query),
                             ("products", Product.query),
                             ("categories", Category.query)):
                n = q.delete()
                print(f"   deleted {n:4d} {label}")
            db.session.commit()
            print("\nKept: all bills & sales history, users, store name, settings.")

        elif choice == "2":
            for label, q in (("bill lines", SaleItem.query),
                             ("bills", Sale.query),
                             ("stock history", StockMovement.query),
                             ("held bills", HeldBill.query),
                             ("products", Product.query),
                             ("categories", Category.query)):
                n = q.delete()
                print(f"   deleted {n:4d} {label}")
            db.session.commit()
            print("\nKept: users (logins), store name, settings.")

        elif choice == "3":
            db.drop_all()
            db.create_all()
            for key, value in DEFAULT_SETTINGS.items():
                db.session.add(Setting(key=key, value=value))
            admin = User(username="admin", full_name="Store Owner", role="admin")
            admin.set_password("admin123")
            cashier = User(username="cashier", full_name="Cashier", role="cashier")
            cashier.set_password("cashier123")
            db.session.add_all([admin, cashier])
            db.session.commit()
            print("\nEverything was wiped and rebuilt from zero:")
            print("  Logins: admin / admin123  and  cashier / cashier123")
            print("    -> CHANGE these passwords in Settings!")
            print("  Settings are back to defaults (check store name, address...).")

        elif choice == "4":
            for label, q in (("bill lines", SaleItem.query),
                             ("bills", Sale.query),
                             ("stock history", StockMovement.query),
                             ("held bills", HeldBill.query)):
                n = q.delete()
                print(f"   deleted {n:4d} {label}")
            db.session.commit()
            print("\nKept: products (with their CURRENT stock numbers), categories,")
            print("      photos, users (logins), store name, settings.")
            print("\nNOTE: stock quantities were NOT changed by this reset.")
            print("      If test bills reduced stock and you want those units")
            print("      back, fix the numbers via Inventory -> Adjust, or use")
            print("      the Excel import with 'Update existing products' ticked.")

        show_counts("\nAFTER - what is in the database now:")

        # Photos only become unused when products are deleted (options 1-3)
        if choice in ("1", "2", "3"):
            up = ROOT / "uploads" / "products"
            if up.is_dir() and any(up.iterdir()):
                ans = input("\nAlso delete all product PHOTOS on disk? (y/N): ").strip().lower()
                if ans == "y":
                    removed = 0
                    for f in up.iterdir():
                        try:
                            f.unlink()
                            removed += 1
                        except OSError:
                            pass
                    print(f"Deleted {removed} photo file(s).")
                else:
                    print("Photos kept in uploads\\products (they are simply unused).")

    print("\nDone! Start the app again with run.bat, then press Ctrl+F5 in the browser.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("\nUNEXPECTED ERROR - nothing may have been changed.")
        print("Please send the text below to me:")
        print("-" * 62)
        import traceback
        traceback.print_exc()
        print("-" * 62)
    finally:
        input("\nPress Enter to close...")