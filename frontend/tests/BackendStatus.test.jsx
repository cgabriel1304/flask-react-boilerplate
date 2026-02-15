import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router-dom'
import { ChakraProvider, defaultSystem } from '@chakra-ui/react'
import { configureStore } from '@reduxjs/toolkit'
import healthReducer from '../src/store/healthSlice'
import BackendStatus from '../src/pages/BackendStatus'

function renderBackendStatus(store) {
  const testStore = store || configureStore({ reducer: { health: healthReducer } })
  return render(
    <Provider store={testStore}>
      <MemoryRouter>
        <ChakraProvider value={defaultSystem}>
          <BackendStatus />
        </ChakraProvider>
      </MemoryRouter>
    </Provider>
  )
}

describe('BackendStatus', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the heading', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: 'healthy', message: 'running' }),
    })

    renderBackendStatus()
    expect(screen.getByRole('heading', { name: /backend status/i })).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByText(/healthy/)).toBeInTheDocument()
    })
  })

  it('displays health data after successful fetch', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: 'healthy', message: 'Cyberitance backend is running' }),
    })

    renderBackendStatus()

    await waitFor(() => {
      expect(screen.getByText(/healthy/)).toBeInTheDocument()
    })
    expect(screen.getByText(/Cyberitance backend is running/)).toBeInTheDocument()
  })

  it('shows error message on fetch failure', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('Network error'))

    renderBackendStatus()

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })

  it('shows error when server returns non-ok response', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: false,
      status: 500,
    })

    renderBackendStatus()

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })

  it('re-fetches when refresh button is clicked', async () => {
    const user = userEvent.setup()
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: 'healthy', message: 'running' }),
    })

    renderBackendStatus()

    await waitFor(() => {
      expect(fetchSpy).toHaveBeenCalledTimes(1)
    })

    await user.click(screen.getByRole('button', { name: /refresh/i }))

    await waitFor(() => {
      expect(fetchSpy).toHaveBeenCalledTimes(2)
    })
  })

  it('renders a link back to home', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ status: 'healthy', message: 'running' }),
    })

    renderBackendStatus()
    expect(screen.getByRole('link', { name: /back to home/i })).toHaveAttribute('href', '/')
    await waitFor(() => {
      expect(screen.getByText(/healthy/)).toBeInTheDocument()
    })
  })
})
