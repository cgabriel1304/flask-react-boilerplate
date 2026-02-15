# Testing Guidelines

## Backend (pytest)

### Running Tests

```bash
cd backend

pytest                          # all tests
pytest tests/test_app.py        # single file
pytest tests/test_app.py::TestHealthCheck  # single class
pytest -k "test_health"         # by name pattern
pytest --cov                    # with coverage report
pytest -v                       # verbose output
```

### Test Location & Naming

- All tests live in `backend/tests/`
- Name files `test_<module>.py` matching the source module (e.g., `test_app.py` for `app.py`)
- Name test functions `test_<behavior>` — describe what is being verified, not the method name
- Group related tests in classes prefixed with `Test` (e.g., `TestHealthCheck`)

### Fixtures (defined in `conftest.py`)

| Fixture | Scope | Description |
|---|---|---|
| `app` | session | Flask app created with `TestingConfig` (SQLite in-memory) |
| `client` | function | Flask test client for HTTP requests |
| `db` | function (autouse) | Creates all tables before test, drops them after |

The `db` fixture is autouse — it runs for every test automatically. You don't need to request it unless you need direct database access in your test.

### Writing Endpoint Tests

Use the `client` fixture to test API endpoints:

```python
class TestUsers:
    def test_create_user(self, client):
        response = client.post('/api/users', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == 'testuser'

    def test_create_user_missing_field(self, client):
        response = client.post('/api/users', json={'username': 'testuser'})
        assert response.status_code == 400
```

### Writing Model Tests

Use `app.app_context()` for database operations and call `db.create_all()` to ensure tables exist:

```python
def test_user_to_dict(self, app):
    with app.app_context():
        db.create_all()
        user = User(username='test', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        data = user.to_dict()
        assert data['username'] == 'test'
```

### Test Database

Tests use `TestingConfig` which sets `SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'`. No PostgreSQL is required to run tests. Each test gets a fresh database via the autouse `db` fixture.

### Adding New Test Fixtures

Add shared fixtures to `tests/conftest.py`. For fixtures specific to one test file, define them at the top of that file.

---

## Frontend (Vitest)

### Running Tests

```bash
cd frontend

npm run test           # run all tests once
npm run test:watch     # watch mode (re-runs on file changes)
npx vitest run tests/App.test.jsx  # single file
```

### Test Location & Naming

- All tests live in `frontend/tests/`
- Name files `<Component>.test.jsx` matching the source component
- Use `describe` blocks to group by component, `it` blocks for individual behaviors

### Test Setup

- **Config**: Vitest is configured in `vite.config.js` under the `test` key
- **Environment**: `jsdom` — simulates a browser DOM
- **Globals**: `true` — `describe`, `it`, `expect` are available without imports (can still import explicitly)
- **Setup file**: `tests/setup.js` imports `@testing-library/jest-dom` for DOM matchers

### Available Libraries

| Library | Purpose |
|---|---|
| `vitest` | Test runner and assertions |
| `@testing-library/react` | `render`, `screen` queries for component testing |
| `@testing-library/jest-dom` | DOM matchers (`toBeInTheDocument`, `toHaveAttribute`, etc.) |
| `@testing-library/user-event` | Simulating user interactions (clicks, typing) |

### Writing Component Tests

```jsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import MyComponent from '../src/MyComponent'

describe('MyComponent', () => {
  it('renders the title', () => {
    render(<MyComponent />)
    expect(screen.getByText('My Title')).toBeInTheDocument()
  })

  it('handles click events', async () => {
    const user = userEvent.setup()
    render(<MyComponent />)
    await user.click(screen.getByRole('button', { name: /submit/i }))
    expect(screen.getByText('Submitted')).toBeInTheDocument()
  })
})
```

### Query Priority

Follow Testing Library's query priority — prefer queries that reflect how users interact with the page:

1. `getByRole` — buttons, links, headings (best)
2. `getByLabelText` — form inputs
3. `getByPlaceholderText` — inputs without labels
4. `getByText` — non-interactive text content
5. `getByAltText` — images
6. `getByTestId` — last resort

### Testing Components with Providers

Components using Redux, Router, or Chakra UI need their providers in tests. Create a wrapper:

```jsx
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router-dom'
import { ChakraProvider } from '@chakra-ui/react'
import { configureStore } from '@reduxjs/toolkit'

function renderWithProviders(ui, { store, route = '/' } = {}) {
  const testStore = store || configureStore({ reducer: {} })
  return render(
    <Provider store={testStore}>
      <MemoryRouter initialEntries={[route]}>
        <ChakraProvider>{ui}</ChakraProvider>
      </MemoryRouter>
    </Provider>
  )
}
```

### Static Asset Imports

The `vite.config.js` aliases `/vite.svg` to the actual file path so tests can resolve absolute public imports. If you add new absolute imports from `public/`, add corresponding aliases in the `resolve.alias` config.

---

## General Principles

- Test behavior, not implementation — assert on what the user sees or what the API returns
- One assertion concern per test — a test can have multiple `assert`/`expect` calls if they verify the same behavior
- Use descriptive test names that read as specifications (e.g., `test_create_user_missing_field` not `test_create_user_2`)
- Keep tests independent — no test should depend on another test's side effects
- Don't test framework internals — trust Flask's routing, React's rendering, SQLAlchemy's ORM
