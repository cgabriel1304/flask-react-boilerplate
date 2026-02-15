import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router-dom'
import { ChakraProvider, defaultSystem } from '@chakra-ui/react'
import { configureStore } from '@reduxjs/toolkit'
import healthReducer from '../src/store/healthSlice'
import App from '../src/App'

function renderApp(route = '/') {
  const store = configureStore({ reducer: { health: healthReducer } })
  return render(
    <Provider store={store}>
      <MemoryRouter initialEntries={[route]}>
        <ChakraProvider value={defaultSystem}>
          <App />
        </ChakraProvider>
      </MemoryRouter>
    </Provider>
  )
}

describe('App', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: 'healthy', message: 'running' }),
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the home page by default', () => {
    renderApp()
    expect(screen.getByRole('heading', { name: /cyberitance/i })).toBeInTheDocument()
  })

  it('renders a link to the status page', () => {
    renderApp()
    expect(screen.getByRole('link', { name: /backend status/i })).toBeInTheDocument()
  })

  it('navigates to the status page when link is clicked', async () => {
    const user = userEvent.setup()
    renderApp()

    await user.click(screen.getByRole('link', { name: /backend status/i }))
    expect(screen.getByRole('heading', { name: /backend status/i })).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByText(/healthy/)).toBeInTheDocument()
    })
  })

  it('renders the status page directly', async () => {
    renderApp('/status')
    expect(screen.getByRole('heading', { name: /backend status/i })).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByText(/healthy/)).toBeInTheDocument()
    })
  })
})
