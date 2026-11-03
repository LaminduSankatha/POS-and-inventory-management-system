"""Packages this project into grocery_store.zip (skips venv, caches, database, backups)."""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"venv", "__pycache__", ".git", ".pytest_cache", "database", "backups", "uploads"}
SKIP_FILES = {"grocery_store.zip", ".env"}

def main():
    out = ROOT / "grocery_store.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(ROOT.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(ROOT)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            if path.name in SKIP_FILES:
                continue
            z.write(path, Path("grocery_store") / rel)
            count += 1
    print(f"Created {out.name} with {count} files.")
    print("The database, product images and backups are created automatically on first run.")

if __name__ == "__main__":
    main()
