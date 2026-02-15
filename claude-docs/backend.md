# Backend Guidelines

## Stack

- Flask 3.0 with application factory pattern
- Python 3.9+
- PostgreSQL via psycopg
- python-dotenv for environment variables
- pytest for testing
- black, flake8, isort for code quality

## Application Structure

### App Factory

`app.py` contains `create_app(config_name)` which:
1. Creates the Flask instance with `static_folder='public'`
2. Loads config from `config.py` based on `FLASK_ENV`
3. Initializes SQLAlchemy (`db` from `db/`)
4. Calls `register_routes(app)` from `routes/` to register all blueprints
5. Calls `db.create_all()` in app context

Always use the factory — never instantiate Flask directly in new code.

### Configuration

`config.py` defines three classes inheriting from `Config`:
- `DevelopmentConfig` — `DEBUG=True`, `SQLALCHEMY_ECHO=True`, PostgreSQL
- `TestingConfig` — `TESTING=True`, SQLite in-memory
- `ProductionConfig` — `DEBUG=False`, reads `DATABASE_URL` from env

Selected by the `FLASK_ENV` env var (`development`, `testing`, `production`).

### Adding Routes

Routes use Flask Blueprints organized under the `routes/` package:

- **API routes** go in `routes/api/` — create a new file (e.g., `routes/api/users.py`), define routes on `api_bp`, and import the module in `routes/api/__init__.py`.
- **Static/frontend routes** go in `routes/static/__init__.py` on `static_bp`.
- All blueprints are registered by `register_routes(app)` in `routes/__init__.py`.

All API endpoints must be under the `/api` prefix to work with the Vite proxy. The prefix is applied when `api_bp` is registered in `routes/__init__.py`.

See [Project Structure](project-structure.md) for detailed how-to guides.

### Route Conventions

- Return JSON responses using `jsonify()`
- Use HTTP status codes explicitly: `return jsonify({...}), 201`
- Use Flask's `request` object for input; validate at the boundary
- Group related endpoints in separate Blueprint modules as the app grows

### Route Logging

Each blueprint has a `before_request` hook that logs every incoming request with method and path:

- **API routes** (`routes/api/`) — logged at **INFO** level
- **Static routes** (`routes/static/`) — logged at **DEBUG** level

Logging is configured in `create_app()` via `logging.basicConfig()`. In development the root log level is `DEBUG` (so both API and static route logs appear); in production it is `INFO` (static route logs are suppressed).

When adding a new blueprint, follow this pattern to keep logging consistent:

```python
import logging
from flask import Blueprint, request

logger = logging.getLogger(__name__)
my_bp = Blueprint('my_bp', __name__)

@my_bp.before_request
def log_request():
    logger.info('%s %s', request.method, request.path)  # or logger.debug(...)
```

### Static File Serving

Flask serves the built frontend from `backend/public/` via the `static_bp` blueprint in `routes/static/`:
- `GET /` returns `public/index.html`
- Static assets (JS, CSS) served via Flask's static file handler
- Error handlers (404 JSON, 500 with rollback) are registered as `app_errorhandler` on `static_bp`
- If you need SPA client-side routing fallback, update the 404 handler in `routes/static/__init__.py` to serve `index.html` for non-API routes

### WSGI / Production

`wsgi.py` is the production entry point. It creates the app with `FLASK_ENV` (defaults to `production`) and adds `db` to `flask shell` context.

## Testing

### Setup

Tests live in `backend/tests/`. Fixtures in `conftest.py`:
- `app` — session-scoped, uses `TestingConfig` (SQLite in-memory)
- `client` — Flask test client for making requests
- `db` — autouse, creates all tables before each test and drops them after

### Writing Tests

- Name test files `test_*.py` and test functions `test_*`
- Use the `client` fixture for endpoint tests:
  ```python
  def test_health(client):
      response = client.get('/api/health')
      assert response.status_code == 200
      assert response.json['status'] == 'healthy'
  ```
- Use the `db` fixture (injected automatically) when testing model operations
- Tests run against SQLite in-memory — no PostgreSQL needed for CI

### Running Tests

```bash
cd backend
pytest                       # all tests
pytest tests/test_routes.py  # single file
pytest -k "test_health"      # by name pattern
pytest --cov                 # with coverage report
```

## Code Quality

- **black** — formatter, run `black .` from `backend/`
- **flake8** — linter, run `flake8 .`
- **isort** — import sorting, run `isort .`

Run all three before committing. They have no project-specific config files yet — use defaults.

## Environment Files

- `.env` — database credentials, `SECRET_KEY`, loaded by `python-dotenv`
- `.flaskenv` — `FLASK_APP=app.py`, `FLASK_ENV`, `FLASK_DEBUG`, loaded automatically by Flask CLI
- `.env.example` / `.flaskenv.example` — templates for new developers
