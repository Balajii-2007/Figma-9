"""
test_models.py — Unit tests for ORM models.
"""
import pytest
from app.models import Event, Registration
from app.extensions import db


def test_event_creation(app):
    with app.app_context():
        e = Event.query.filter_by(name="Test Marathon").first()
        assert e is not None
        assert e.max_participants == 10


def test_event_spots_left(app):
    with app.app_context():
        e = Event.query.filter_by(name="Test Marathon").first()
        assert e.spots_left == e.max_participants - e.registered_count


def test_event_to_dict(app):
    with app.app_context():
        e = Event.query.first()
        d = e.to_dict()
        assert "name" in d
        assert "spots_left" in d
        assert "is_full" in d


def test_registration_save(app):
    with app.app_context():
        e = Event.query.filter_by(name="Test Marathon").first()
        reg = Registration(full_name="Jane Doe", email="jane@test.com", event_id=e.id)
        db.session.add(reg)
        db.session.commit()
        assert reg.id is not None
        assert reg.event.name == "Test Marathon"
        # cleanup
        db.session.delete(reg)
        db.session.commit()


def test_event_full(app):
    with app.app_context():
        e = Event.query.filter_by(name="Test Basketball").first()
        # Fill all spots
        regs = [
            Registration(full_name=f"Player {i}", email=f"p{i}@test.com", event_id=e.id)
            for i in range(e.max_participants)
        ]
        db.session.add_all(regs)
        db.session.commit()
        assert e.is_full is True
        # cleanup
        for r in regs:
            db.session.delete(r)
        db.session.commit()
