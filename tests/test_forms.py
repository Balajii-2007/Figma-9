"""
test_forms.py — Unit tests for form validation logic.
"""
from app.forms import validate_user_form, validate_registration_form


# ── validate_user_form ──────────────────────────────────────────

def test_user_form_valid():
    valid, errors = validate_user_form({"full_name": "Alice", "email": "alice@example.com"})
    assert valid is True
    assert errors == {}


def test_user_form_missing_name():
    valid, errors = validate_user_form({"full_name": "", "email": "alice@example.com"})
    assert valid is False
    assert "full_name" in errors


def test_user_form_short_name():
    valid, errors = validate_user_form({"full_name": "A", "email": "alice@example.com"})
    assert valid is False
    assert "full_name" in errors


def test_user_form_missing_email():
    valid, errors = validate_user_form({"full_name": "Alice", "email": ""})
    assert valid is False
    assert "email" in errors


def test_user_form_invalid_email():
    valid, errors = validate_user_form({"full_name": "Alice", "email": "not-an-email"})
    assert valid is False
    assert "email" in errors


# ── validate_registration_form ──────────────────────────────────

def test_registration_form_valid():
    valid, errors = validate_registration_form(
        {"full_name": "Bob", "email": "bob@example.com", "event_id": "1"}
    )
    assert valid is True


def test_registration_form_missing_event():
    valid, errors = validate_registration_form(
        {"full_name": "Bob", "email": "bob@example.com", "event_id": ""}
    )
    assert valid is False
    assert "event_id" in errors
