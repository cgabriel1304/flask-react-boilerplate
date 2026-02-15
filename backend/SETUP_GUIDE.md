"""Backend API setup and initialization guide"""

# Backend folder structure:
# backend/
# ├── .env                    # Environment variables (database credentials, secret keys)
# ├── .flaskenv              # Flask-specific environment
# ├── .gitignore             # Git ignore rules
# ├── alembic.ini            # Alembic configuration
# ├── app.py                 # Flask application factory
# ├── config.py              # Configuration classes
# ├── models.py              # SQLAlchemy ORM models
# ├── routes.py              # API routes and blueprints
# ├── wsgi.py                # WSGI entry point for production
# ├── requirements.txt       # Python dependencies
# ├── requirements-dev.txt   # Development dependencies
# ├── .venv/                 # Virtual environment (auto-created)
# ├── migrations/            # Alembic migrations
# │   ├── env.py
# │   ├── script.py.mako
# │   └── versions/
# ├── utils/                 # Utility modules
# │   └── __init__.py
# ├── tests/                 # Test suite
# │   ├── __init__.py
# │   └── conftest.py
# └── static/                # Frontend build output

# Quick Start Commands:
# 1. Create virtual environment: python -m venv .venv
# 2. Activate: .venv\Scripts\activate (Windows)
# 3. Install dependencies: pip install -r requirements.txt
# 4. Run migrations: alembic upgrade head
# 5. Start server: flask run

print("Backend structure initialized!")
