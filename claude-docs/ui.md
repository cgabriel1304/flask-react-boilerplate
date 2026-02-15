# UI Guidelines

## Stack

- React 19 with JSX (no TypeScript)
- Chakra UI v3 with Emotion for styling
- Redux Toolkit + react-redux for state management
- react-router-dom v7 for routing
- Framer Motion for animations
- Vite 7 as build tool

## Component Patterns

### File Structure

Place components in `frontend/src/`. Group by feature when the app grows:

```
src/
├── components/       # Shared/reusable components
├── pages/            # Route-level components
├── store/            # Redux slices and store config
├── hooks/            # Custom React hooks
├── utils/            # Helper functions
├── assets/           # Static assets (images, SVGs)
├── App.jsx           # Root component, router setup
├── main.jsx          # Entry point, renders <App /> in StrictMode
└── index.css         # Global styles
```

### Component Conventions

- Use functional components with hooks exclusively (no class components)
- File naming: PascalCase for components (`UserProfile.jsx`), camelCase for utilities (`formatDate.js`)
- One component per file; export as default
- Wrap the app in `<StrictMode>` (already set up in `main.jsx`)

### Chakra UI v3

- Use Chakra components for all layout and UI elements instead of raw HTML
- Chakra v3 uses the `@chakra-ui/react` package — do not import from sub-packages like `@chakra-ui/layout`
- Use Chakra's built-in responsive props (`{{ base: "sm", md: "lg" }}`) over custom media queries
- Use Chakra's color mode system for light/dark theme support

### State Management

- Use Redux Toolkit's `createSlice` for state slices — avoid legacy Redux patterns (`switch` reducers, manual action creators)
- Use `createAsyncThunk` for API calls that need loading/error states
- Keep component-local state in `useState`/`useReducer`; only lift to Redux when state is shared across unrelated components
- Configure the store in `src/store/` and provide it via `<Provider>` in `main.jsx`

### Routing

- Define routes in `App.jsx` using react-router-dom v7's `<Routes>` and `<Route>`
- Use `<Link>` and `useNavigate()` for navigation — never use `window.location` for internal routes
- All routes are client-side; Flask handles the SPA fallback in production

### API Calls

- All backend requests go through the `/api` prefix (e.g., `/api/health`, `/api/users`)
- In development, Vite proxies `/api` to `http://localhost:5000` — use relative URLs, not absolute
- Use `fetch` or Redux Toolkit's `createAsyncThunk` for API calls
- Handle loading and error states in the UI

## Linting

- ESLint flat config in `eslint.config.js`
- Rules: `no-unused-vars` errors (except uppercase constants matching `^[A-Z_]`)
- React Hooks rules enforced via `eslint-plugin-react-hooks`
- Run with `npm run lint` from `frontend/`

## Build Output

- `npm run build` compiles to `../backend/public/` (configured in `vite.config.js`)
- `emptyOutDir: true` — each build wipes the previous output
- Do not manually edit files in `backend/public/`; they are generated artifacts
