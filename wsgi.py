"""
wsgi.py — Production WSGI entry point.

Usage with Gunicorn:
    gunicorn "wsgi:app" --bind 0.0.0.0:8000 --workers 4
"""
from app import create_app

app = create_app("production")

if __name__ == "__main__":
    app.run()
