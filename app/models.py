"""
models.py — SQLAlchemy ORM models.
"""
from datetime import datetime
from .extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(120), nullable=False)
    date             = db.Column(db.String(60),  nullable=False)
    venue            = db.Column(db.String(120), nullable=False)
    category         = db.Column(db.String(60),  nullable=False)
    icon             = db.Column(db.String(10),  nullable=False, default="🏆")
    max_participants = db.Column(db.Integer,     nullable=False, default=100)
    description      = db.Column(db.Text,        nullable=True)

    registrations    = db.relationship("Registration", backref="event", lazy=True,
                                       cascade="all, delete-orphan")

    @property
    def registered_count(self):
        return len(self.registrations)

    @property
    def spots_left(self):
        return max(0, self.max_participants - self.registered_count)

    @property
    def is_full(self):
        return self.spots_left == 0

    def to_dict(self):
        return {
            "id":               self.id,
            "name":             self.name,
            "date":             self.date,
            "venue":            self.venue,
            "category":         self.category,
            "icon":             self.icon,
            "max_participants": self.max_participants,
            "registered_count": self.registered_count,
            "spots_left":       self.spots_left,
            "is_full":          self.is_full,
            "description":      self.description,
        }

    def __repr__(self):
        return f"<Event {self.name!r}>"


class Registration(db.Model):
    __tablename__ = "registrations"

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(120), nullable=False)
    phone         = db.Column(db.String(20),  nullable=True)
    event_id      = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("email", "event_id", name="uq_email_event"),
    )

    def to_dict(self):
        return {
            "id":            self.id,
            "full_name":     self.full_name,
            "email":         self.email,
            "phone":         self.phone,
            "event_id":      self.event_id,
            "event_name":    self.event.name if self.event else None,
            "registered_at": self.registered_at.isoformat(),
        }

    def __repr__(self):
        return f"<Registration {self.full_name!r} → {self.event_id}>"
