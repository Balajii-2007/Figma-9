"""
routes/events.py — Event listing & registration (Screen 2).
"""
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for, flash, jsonify, abort)
from ..extensions import db
from ..models import Event, Registration
from ..forms import validate_registration_form

events_bp = Blueprint("events", __name__)


@events_bp.route("/")
def list_events():
    """Screen 2 — Browse available events."""
    if not session.get("user_name"):
        return redirect(url_for("main.index"))

    events = Event.query.order_by(Event.id).all()
    return render_template("events.html",
                           events=events,
                           user_name=session.get("user_name"))


@events_bp.route("/register", methods=["POST"])
def register():
    """Handle event registration form submission."""
    data = {
        "full_name": session.get("user_name", ""),
        "email":     session.get("user_email", ""),
        "event_id":  request.form.get("event_id"),
    }

    valid, errors = validate_registration_form(data)
    if not valid:
        flash("Please fix the errors and try again.", "error")
        return redirect(url_for("events.list_events"))

    event = Event.query.get_or_404(int(data["event_id"]))

    if event.is_full:
        flash(f"Sorry, {event.name} is fully booked.", "error")
        return redirect(url_for("events.list_events"))

    # Prevent duplicate registration
    existing = Registration.query.filter_by(
        email=data["email"], event_id=event.id
    ).first()
    if existing:
        flash("You are already registered for this event.", "warning")
        return redirect(url_for("events.list_events"))

    reg = Registration(
        full_name=data["full_name"],
        email=data["email"],
        event_id=event.id,
    )
    db.session.add(reg)
    db.session.commit()

    session["registered_event"] = event.name
    return redirect(url_for("main.success"))


@events_bp.route("/api/list")
def api_list():
    """JSON API — returns all events."""
    events = Event.query.order_by(Event.id).all()
    return jsonify([e.to_dict() for e in events])
