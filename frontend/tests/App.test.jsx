import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import App from '../src/App'

describe('App', () => {
  it('renders the heading', () => {
    render(<App />)
    expect(screen.getByText('Vite + React')).toBeInTheDocument()
  })

  it('renders Vite and React logos', () => {
    render(<App />)
    expect(screen.getByAltText('Vite logo')).toBeInTheDocument()
    expect(screen.getByAltText('React logo')).toBeInTheDocument()
  })

  it('renders the counter button with initial count of 0', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /count is 0/i })).toBeInTheDocument()
  })

  it('increments count on button click', async () => {
    const user = userEvent.setup()
    render(<App />)

    const button = screen.getByRole('button', { name: /count is 0/i })
    await user.click(button)
    expect(screen.getByRole('button', { name: /count is 1/i })).toBeInTheDocument()
  })

  it('increments count multiple times', async () => {
    const user = userEvent.setup()
    render(<App />)

    const button = screen.getByRole('button', { name: /count is 0/i })
    await user.click(button)
    await user.click(button)
    await user.click(button)
    expect(screen.getByRole('button', { name: /count is 3/i })).toBeInTheDocument()
  })

  it('renders links to Vite and React docs', () => {
    render(<App />)
    const viteLink = screen.getByAltText('Vite logo').closest('a')
    const reactLink = screen.getByAltText('React logo').closest('a')
    expect(viteLink).toHaveAttribute('href', 'https://vite.dev')
    expect(reactLink).toHaveAttribute('href', 'https://react.dev')
  })

  it('opens doc links in new tab', () => {
    render(<App />)
    const viteLink = screen.getByAltText('Vite logo').closest('a')
    const reactLink = screen.getByAltText('React logo').closest('a')
    expect(viteLink).toHaveAttribute('target', '_blank')
    expect(reactLink).toHaveAttribute('target', '_blank')
  })

  it('renders HMR instruction text', () => {
    render(<App />)
    expect(screen.getByText(/Edit/)).toBeInTheDocument()
    expect(screen.getByText('src/App.jsx')).toBeInTheDocument()
  })
})
