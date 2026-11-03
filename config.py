"""Central configuration. Reads an optional .env file (see .env.example)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def _load_env(path=BASE_DIR / ".env"):
    """Tiny .env loader so parents never need extra packages."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

_load_env()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-local-9f3kz82m1v")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'database' / 'grocery.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_FILE = BASE_DIR / "database" / "grocery.db"
    UPLOAD_FOLDER = BASE_DIR / "uploads" / "products"
    BACKUP_FOLDER = BASE_DIR / "backups"

    ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp", "gif", "svg"}
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB uploads (photos are shrunk automatically on save)

    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", "5000"))
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"