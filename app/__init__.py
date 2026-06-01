"""
app/__init__.py — Application Factory
"""
import os
from flask import Flask
from .extensions import db
from .config import config_map


def create_app(config_name=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    env = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_map.get(env, config_map["development"]))

    db.init_app(app)

    # Blueprints
    from .routes.main   import main_bp
    from .routes.events import events_bp
    from .routes.auth   import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(auth_bp,   url_prefix="/auth")

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        from .models import Event, Registration
        return {"db": db, "Event": Event, "Registration": Registration}

    from .errors import register_error_handlers
    register_error_handlers(app)

    return app
