"""
routes/main.py — Main / home routes (Screen 1: registration entry).
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..forms import validate_user_form

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """Screen 1 — Collect name & email, then redirect to events."""
    if request.method == "POST":
        data = {
            "full_name": request.form.get("full_name", "").strip(),
            "email":     request.form.get("email", "").strip(),
        }
        valid, errors = validate_user_form(data)
        if not valid:
            return render_template("index.html", errors=errors, form=data)

        session["user_name"]  = data["full_name"]
        session["user_email"] = data["email"]
        return redirect(url_for("events.list_events"))

    return render_template("index.html", errors={}, form={})


@main_bp.route("/success")
def success():
    """Screen 3 — Registration confirmation."""
    event_name = session.get("registered_event", "the event")
    user_name  = session.get("user_name", "Participant")
    return render_template("success.html", event_name=event_name, user_name=user_name)
