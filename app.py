"""Entry point. Normally started by run.bat — equivalent to: python app.py"""
from app import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)