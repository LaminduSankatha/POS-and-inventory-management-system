"""Checks every required file exists AND that all Python files compile without errors."""
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED = [
    "app.py", "config.py", "init_db.py", "requirements.txt", "run.bat",
    "app/__init__.py", "app/extensions.py", "app/models.py", "app/utils.py",
    "app/routes/__init__.py", "app/routes/auth.py", "app/routes/main.py",
    "app/routes/products.py", "app/routes/categories.py", "app/routes/billing.py",
    "app/routes/inventory.py", "app/routes/sales.py", "app/routes/reports.py",
    "app/routes/settings.py",
    "app/services/__init__.py", "app/services/billing_service.py",
    "app/services/report_service.py", "app/services/backup_service.py",
    "app/templates/base.html", "app/templates/login.html", "app/templates/dashboard.html",
    "app/templates/billing.html", "app/templates/products.html",
    "app/templates/product_form.html", "app/templates/categories.html",
    "app/templates/inventory.html", "app/templates/movements.html",
    "app/templates/sales_history.html", "app/templates/sale_detail.html",
    "app/templates/reports.html", "app/templates/daily_closing.html",
    "app/templates/settings.html",
    "app/static/css/style.css", "app/static/js/main.js",
    "app/static/js/billing.js", "app/static/js/receipt.js",
    "app/static/images/placeholder.svg",
]

print("=" * 60)
print("STEP 1: File presence check")
print("=" * 60)
problems = 0
for rel in REQUIRED:
    if (ROOT / rel).exists():
        continue
    problems += 1
    suspects = list(ROOT.glob(rel + ".*"))
    if suspects:
        print(f"  WRONG NAME : {rel}  (saved as: {', '.join(s.name for s in suspects)})")
    else:
        print(f"  MISSING    : {rel}")
if problems == 0:
    print("  All required files present.")

print()
print("=" * 60)
print("STEP 2: Python syntax check")
print("=" * 60)
bad = 0
for py in sorted(ROOT.rglob("*.py")):
    rel = py.relative_to(ROOT)
    if "venv" in rel.parts or "__pycache__" in rel.parts:
        continue
    try:
        py_compile.compile(str(py), doraise=True)
    except py_compile.PyCompileError as exc:
        bad += 1
        print(f"  BROKEN: {rel}")
        print("    " + str(exc).strip().splitlines()[-1])
if bad == 0:
    print("  All Python files compile cleanly.")

print()
if problems == 0 and bad == 0:
    print("EVERYTHING LOOKS GOOD.")
    print("If the app still fails, copy the last lines of the")
    print("black window error and send them to me.")
input("\nPress Enter to close...")