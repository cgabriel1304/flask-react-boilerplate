# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack Flask + React monorepo. Flask backend serves a React frontend (built by Vite into `backend/public/`). PostgreSQL database with SQLAlchemy ORM and Alembic migrations.

## Common Commands

### Backend (run from `backend/`)

```bash
# Activate virtualenv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt   # adds pytest, black, flake8, isort

# Run dev server (port 5000)
flask run

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1

# Testing
pytest                    # run all tests
pytest tests/test_foo.py  # run single file
pytest -k "test_name"     # run by name
pytest --cov              # with coverage

# Linting & formatting
black .
flake8 .
isort .
```

### Frontend (run from `frontend/`)

```bash
npm install
npm run dev       # dev server on port 5173
npm run build     # builds to ../backend/public/
npm run lint      # eslint
npm run test      # run all tests once (vitest)
npm run test:watch  # watch mode
npm run preview   # preview production build
```

## Architecture

### Backend (`backend/`)

- **`app.py`** — Application factory (`create_app()`), imports `db` from `db/` and calls `register_routes()` from `routes/`
- **`config.py`** — Config classes keyed by `FLASK_ENV`: `DevelopmentConfig` (PostgreSQL), `TestingConfig` (SQLite in-memory), `ProductionConfig`
- **`db/`** — Database package: `__init__.py` exports the `SQLAlchemy` instance (`db`), `models.py` contains `BaseModel` and all model definitions
- **`routes/`** — Route package: `__init__.py` exports `register_routes(app)`, `api/` contains API blueprint and endpoint modules, `static/` serves frontend and error handlers
- **`wsgi.py`** — Production WSGI entry point, also provides `flask shell` context
- **`migrations/`** — Alembic migrations directory (versions currently empty)
- **`tests/conftest.py`** — Pytest fixtures: `app` (session-scoped, uses `TestingConfig`), `client`, `db` (autouse, creates/drops tables per test)

### Frontend (`frontend/`)

- React 19 + Vite 7 + JSX (no TypeScript)
- State: Redux Toolkit + react-redux
- Routing: react-router-dom v7
- UI: Chakra UI v3 + Emotion + Framer Motion
- Entry: `src/main.jsx` → `src/App.jsx`

### Frontend-Backend Integration

- Vite dev server proxies `/api` requests to `http://localhost:5000`
- `npm run build` outputs to `backend/public/`, which Flask serves as static files
- Development requires two terminals (Flask on 5000 + Vite on 5173)
- Production: single Flask server serves both API and built frontend

## Database

- PostgreSQL in dev/prod, SQLite in-memory for tests
- Connection configured via `DATABASE_URL` env var in `backend/.env`
- Config falls back to `postgresql://cyberitance:cyberitance_pass@localhost:5432/cyberitance`

## Guidelines

Detailed guidelines for working in each area of the codebase:

- **[Project Structure](claude-docs/project-structure.md)** — `db/` and `routes/` package layout, how to add models, API routes, and static routes
- **[UI Guidelines](claude-docs/ui.md)** — React component patterns, Chakra UI v3 usage, Redux Toolkit state management, routing, API calls, and linting rules
- **[Backend Guidelines](claude-docs/backend.md)** — Flask app factory, blueprint registration, route conventions, testing setup and patterns, code quality tools
- **[Models & Database Guidelines](claude-docs/models-and-database.md)** — BaseModel inheritance, creating new models, Alembic migration workflow, session management, naming conventions
- **[Testing Guidelines](claude-docs/tests.md)** — pytest fixtures and patterns (backend), Vitest + Testing Library setup (frontend), query priority, provider wrappers, general testing principles

## Prerequisites

- Python 3.9+, Node.js 18+, PostgreSQL 12+
