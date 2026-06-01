"""
extensions.py — Shared Flask extensions (instantiated once, init_app later).
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
