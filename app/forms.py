"""
forms.py — Form validation (pure Python, no WTForms dependency).
"""
import re
from typing import Dict, Tuple, List


def _required(value: str, field: str, errors: Dict):
    if not value or not value.strip():
        errors[field] = f"{field.replace('_', ' ').title()} is required."
        return False
    return True


def _min_length(value: str, field: str, length: int, errors: Dict):
    if len(value.strip()) < length:
        errors[field] = f"{field.replace('_', ' ').title()} must be at least {length} characters."
        return False
    return True


def _valid_email(value: str, errors: Dict):
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    if not re.match(pattern, value.strip()):
        errors["email"] = "Please enter a valid email address."
        return False
    return True


def validate_user_form(data: Dict) -> Tuple[bool, Dict]:
    """Validate name + email before showing events."""
    errors: Dict[str, str] = {}
    name  = data.get("full_name", "")
    email = data.get("email", "")

    if _required(name, "full_name", errors):
        _min_length(name, "full_name", 2, errors)
    if _required(email, "email", errors):
        _valid_email(email, errors)

    return len(errors) == 0, errors


def validate_registration_form(data: Dict) -> Tuple[bool, Dict]:
    """Validate full registration submission."""
    errors: Dict[str, str] = {}
    name     = data.get("full_name", "")
    email    = data.get("email", "")
    event_id = data.get("event_id", "")

    if _required(name, "full_name", errors):
        _min_length(name, "full_name", 2, errors)
    if _required(email, "email", errors):
        _valid_email(email, errors)
    if not event_id:
        errors["event_id"] = "Please select an event."

    return len(errors) == 0, errors
