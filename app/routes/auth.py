"""
routes/auth.py — Session management (logout / clear session).
"""
from flask import Blueprint, session, redirect, url_for

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/logout")
def logout():
    """Clear session and return to home."""
    session.clear()
    return redirect(url_for("main.index"))
