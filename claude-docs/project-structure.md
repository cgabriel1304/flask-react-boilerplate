# Project Structure

## Backend Package Layout

```
backend/
├── app.py                     # Application factory (create_app)
├── config.py                  # Config classes by environment
├── wsgi.py                    # Production WSGI entry point
├── db/
│   ├── __init__.py            # SQLAlchemy instance (db)
│   └── models.py              # BaseModel and all model definitions
├── routes/
│   ├── __init__.py            # register_routes(app) — registers all blueprints
│   ├── api/
│   │   ├── __init__.py        # api_bp Blueprint, imports sub-modules
│   │   ├── health.py          # /api/health endpoint
│   │   └── status.py          # /api/status endpoint
│   └── static/
│       └── __init__.py        # static_bp Blueprint (index route + error handlers)
├── migrations/                # Alembic migrations
├── tests/                     # pytest test suite
└── public/                    # Built frontend (output of npm run build)
```

## Key Packages

### `db/` — Database Layer

- `db/__init__.py` exports the `db` SQLAlchemy instance. Import it as `from db import db`.
- `db/models.py` contains `BaseModel` and all application models. Import models as `from db.models import BaseModel`.
- The `db` instance is initialized on the app inside `create_app()` via `db.init_app(app)`.

### `routes/` — Route Definitions

- `routes/__init__.py` exports `register_routes(app)` which registers all blueprints on the Flask app.
- `routes/api/` contains the `api_bp` Blueprint (registered with `/api` prefix) and its sub-modules.
- `routes/static/` contains the `static_bp` Blueprint for serving the frontend and handling error responses.

## How To

### Add a New Model

1. Define the model in `db/models.py` inheriting from `BaseModel`
2. Set `__tablename__` explicitly
3. Override `to_dict()` calling `super().to_dict()` and extending with model-specific fields
4. Import the model in `migrations/env.py` so Alembic detects it
5. Run `alembic revision --autogenerate -m "Description"` then `alembic upgrade head`

### Add a New API Route

1. Create a new file in `routes/api/` (e.g., `routes/api/users.py`)
2. Import and use `api_bp` from `routes.api`:
   ```python
   from flask import jsonify
   from routes.api import api_bp

   @api_bp.route('/users', methods=['GET'])
   def list_users():
       return jsonify([]), 200
   ```
3. Import the new module in `routes/api/__init__.py`:
   ```python
   from routes.api import health, status, users  # noqa: E402, F401
   ```
4. The route will be accessible at `/api/users` (the `/api` prefix comes from blueprint registration).

### Add a New Static Route

Add routes to `routes/static/__init__.py` using `static_bp`:
```python
@static_bp.route('/about')
def about():
    return send_from_directory(current_app.static_folder, 'index.html')
```
