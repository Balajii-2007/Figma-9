#!/usr/bin/env python3
"""
manage.py — Sports Event Registration (Flask)
Entry point for all project management commands.

Usage:
    python manage.py runserver
    python manage.py initdb
    python manage.py seeddb
    python manage.py shell
    python manage.py show_routes
    python manage.py list_registrations
"""

import os
import sys
import argparse
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))


# ─────────────────────────────────────────────────────────────────
#  Commands
# ─────────────────────────────────────────────────────────────────

def cmd_runserver(args):
    """Start the Flask development server."""
    os.environ.setdefault("FLASK_ENV", "development")
    os.environ.setdefault("FLASK_DEBUG", "1")

    from app import create_app
    app = create_app()
    print(f"\n  🏃  Sports Event Registration")
    print(f"  ──────────────────────────────────")
    print(f"  http://{args.host}:{args.port}/")
    print(f"  Press CTRL+C to quit\n")
    app.run(host=args.host, port=args.port, debug=True)


def cmd_initdb(args):
    """Create all database tables."""
    from app import create_app
    from app.extensions import db
    app = create_app()
    with app.app_context():
        db.create_all()
        print("  ✅  Database tables created.")
    print(f"  📦  DB path: {BASE_DIR / 'instance' / 'sports.db'}\n")


def cmd_seeddb(args):
    """Seed events into the database."""
    from app import create_app
    from app.extensions import db
    from app.models import Event
    app = create_app()
    with app.app_context():
        if Event.query.count() > 0:
            print("  ℹ️   Events already seeded. Use --force to re-seed.")
            if not args.force:
                return
            Event.query.delete()

        seeds = [
            Event(name="Marathon Championship", date="December 15, 2025",
                  venue="City Sports Complex",  category="Running",
                  icon="🏃", max_participants=500, description="Annual city marathon open to all runners."),
            Event(name="Basketball Tournament", date="January 10, 2026",
                  venue="Downtown Arena",       category="Basketball",
                  icon="🏀", max_participants=16,  description="3x3 knockout tournament."),
            Event(name="Swimming Competition",  date="December 28, 2025",
                  venue="Olympic Pool Center",  category="Swimming",
                  icon="🏊", max_participants=200, description="Multi-discipline aquatic event."),
            Event(name="Football League",       date="February 5, 2026",
                  venue="National Stadium",     category="Football",
                  icon="⚽", max_participants=300, description="5-a-side corporate league."),
            Event(name="Tennis Open",           date="March 12, 2026",
                  venue="Central Tennis Club",  category="Tennis",
                  icon="🎾", max_participants=64,  description="Singles & doubles open draw."),
            Event(name="Cycling Grand Prix",    date="April 3, 2026",
                  venue="Riverside Circuit",    category="Cycling",
                  icon="🚴", max_participants=150, description="Road race around the riverside circuit."),
        ]
        db.session.add_all(seeds)
        db.session.commit()
        print(f"  ✅  {len(seeds)} events seeded.\n")


def cmd_shell(args):
    """Launch an interactive Python shell with app context."""
    from app import create_app
    from app.extensions import db
    from app.models import Event, Registration
    app = create_app()
    with app.app_context():
        import code
        ctx = {"app": app, "db": db, "Event": Event, "Registration": Registration}
        code.interact(local=ctx, banner="\n  Sports Events Shell — ctx: app, db, Event, Registration\n")


def cmd_show_routes(args):
    """Print all registered URL routes."""
    from app import create_app
    app = create_app()
    print(f"\n  {'Method':<10} {'Endpoint':<30} {'URL Rule'}")
    print("  " + "─" * 65)
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"  {methods:<10} {rule.endpoint:<30} {rule.rule}")
    print()


def cmd_list_registrations(args):
    """Display all registrations in a table."""
    from app import create_app
    from app.models import Registration, Event
    app = create_app()
    with app.app_context():
        regs = Registration.query.join(Event).order_by(Registration.registered_at.desc()).all()
        if not regs:
            print("  No registrations yet.\n")
            return
        print(f"\n  {'ID':<5} {'Name':<25} {'Email':<30} {'Event':<25} {'Date'}")
        print("  " + "─" * 100)
        for r in regs:
            print(f"  {r.id:<5} {r.full_name:<25} {r.email:<30} {r.event.name:<25} {str(r.registered_at)[:19]}")
        print()


# ─────────────────────────────────────────────────────────────────
#  CLI Entry
# ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="manage.py",
        description="Sports Event Registration — project manager",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # runserver
    p_srv = sub.add_parser("runserver", help="Start Flask dev server")
    p_srv.add_argument("--host", default="127.0.0.1")
    p_srv.add_argument("--port", type=int, default=5000)

    # initdb
    sub.add_parser("initdb", help="Create database tables")

    # seeddb
    p_seed = sub.add_parser("seeddb", help="Seed event data")
    p_seed.add_argument("--force", action="store_true", help="Re-seed even if data exists")

    # shell
    sub.add_parser("shell", help="Interactive shell with app context")

    # show_routes
    sub.add_parser("show_routes", help="List all URL routes")

    # list_registrations
    sub.add_parser("list_registrations", help="Show all registrations")

    args = parser.parse_args()

    dispatch = {
        "runserver":          cmd_runserver,
        "initdb":             cmd_initdb,
        "seeddb":             cmd_seeddb,
        "shell":              cmd_shell,
        "show_routes":        cmd_show_routes,
        "list_registrations": cmd_list_registrations,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
