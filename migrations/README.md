# Migrations

This project uses a lightweight SQLite setup managed via `manage.py`.

## Commands

```bash
# Create all tables from models
python manage.py initdb

# Seed initial event data
python manage.py seeddb

# Re-seed (drops existing events first)
python manage.py seeddb --force
```

## Adding a New Column (manual migration example)

```python
import sqlite3
conn = sqlite3.connect("instance/sports.db")
conn.execute("ALTER TABLE events ADD COLUMN image_url TEXT")
conn.commit()
conn.close()
```

## Switching to Flask-Migrate (optional)

```bash
pip install Flask-Migrate
# Then in app/__init__.py:
from flask_migrate import Migrate
migrate = Migrate(app, db)
# Run:
flask db init
flask db migrate -m "initial"
flask db upgrade
```
