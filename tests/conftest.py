"""
conftest.py — Pytest fixtures shared across all tests.
"""
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import Event, Registration


@pytest.fixture(scope="session")
def app():
    """Create application with testing config."""
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        _seed_events()
        yield application
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    """Database session scoped per test — rolls back after each."""
    with app.app_context():
        yield _db
        _db.session.rollback()


def _seed_events():
    if Event.query.count() == 0:
        events = [
            Event(name="Test Marathon",    date="Dec 15, 2025", venue="Test Stadium",
                  category="Running",    icon="🏃", max_participants=10),
            Event(name="Test Basketball",  date="Jan 10, 2026", venue="Test Arena",
                  category="Basketball", icon="🏀", max_participants=2),
        ]
        _db.session.add_all(events)
        _db.session.commit()
