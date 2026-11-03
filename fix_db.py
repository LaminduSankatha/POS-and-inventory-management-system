"""One-click repair: adds the newer bill columns to the existing database."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "database" / "grocery.db"


def main():
    if not DB.exists():
        print("Database not found at:", DB)
        print("Start the app once with run.bat (it creates the database), then run this again.")
    else:
        conn = sqlite3.connect(str(DB))
        try:
            cols = [row[1] for row in conn.execute("PRAGMA table_info(sales)")]
            if not cols:
                print("The sales table doesn't exist yet - start run.bat once first.")
            else:
                changed = False
                if "amount_paid" not in cols:
                    conn.execute("ALTER TABLE sales ADD COLUMN amount_paid FLOAT DEFAULT 0")
                    print("Added column: amount_paid")
                    changed = True
                else:
                    print("Already present: amount_paid")
                if "change_given" not in cols:
                    conn.execute("ALTER TABLE sales ADD COLUMN change_given FLOAT DEFAULT 0")
                    print("Added column: change_given")
                    changed = True
                else:
                    print("Already present: change_given")
                if changed:
                    conn.commit()
                    print("\nDatabase repaired successfully!")
                else:
                    print("\nNothing to do - database is already up to date.")
        except Exception as exc:
            print("\nERROR:", exc)
            print("Close the black POS window completely, then run this again.")
        finally:
            conn.close()
        print("\nNow start the app again with run.bat.")
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()