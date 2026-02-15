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
3. Initializes SQLAlchemy (`db`)
4. Registers error handlers (404 JSON, 500 with rollback)
5. Calls `db.create_all()` in app context

Always use the factory — never instantiate Flask directly in new code.

### Configuration

`config.py` defines three classes inheriting from `Config`:
- `DevelopmentConfig` — `DEBUG=True`, `SQLALCHEMY_ECHO=True`, PostgreSQL
- `TestingConfig` — `TESTING=True`, SQLite in-memory
- `ProductionConfig` — `DEBUG=False`, reads `DATABASE_URL` from env

Selected by the `FLASK_ENV` env var (`development`, `testing`, `production`).

### Adding Routes

Routes use Flask Blueprints. The `api_bp` blueprint is defined in `routes.py` but **not yet registered** in `app.py`. To activate it:

1. Uncomment these lines in `app.py`:
   ```python
   from routes import api_bp
   app.register_blueprint(api_bp, url_prefix='/api')
   ```

2. Add new routes to `routes.py` or create new blueprint modules and register them on `api_bp`.

All API endpoints must be under the `/api` prefix to work with the Vite proxy.

### Route Conventions

- Return JSON responses using `jsonify()`
- Use HTTP status codes explicitly: `return jsonify({...}), 201`
- Use Flask's `request` object for input; validate at the boundary
- Group related endpoints in separate Blueprint modules as the app grows

### Static File Serving

Flask serves the built frontend from `backend/public/`:
- `GET /` returns `public/index.html`
- Static assets (JS, CSS) served via Flask's static file handler
- The 404 handler returns JSON — if you need SPA client-side routing fallback, update it to serve `index.html` for non-API routes

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
