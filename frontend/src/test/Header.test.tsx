/**
 * Tests for Header component
 * Following TDD approach - tests written before implementation
 */
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import Header from '../components/Header'

// Mock the contexts
const mockUseCart = vi.fn()
const mockUseAuth = vi.fn()

vi.mock('../contexts/CartContext', () => ({
  useCart: () => mockUseCart()
}))

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => mockUseAuth()
}))

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  )
}

describe('Header', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders site title and navigation', () => {
    // Mock empty cart and no user
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    expect(screen.getByText('Vintage Store')).toBeInTheDocument()
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Products')).toBeInTheDocument()
    expect(screen.getByText('Cart (0)')).toBeInTheDocument()
  })

  it('displays cart item count', () => {
    // Mock cart with items
    mockUseCart.mockReturnValue({
      getItemCount: () => 3
    })
    mockUseAuth.mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    expect(screen.getByText('Cart (3)')).toBeInTheDocument()
  })

  it('shows login button when user is not authenticated', () => {
    // Mock no user
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    expect(screen.getByText('Login')).toBeInTheDocument()
    expect(screen.getByText('Register')).toBeInTheDocument()
  })

  it('shows user menu when user is authenticated', () => {
    // Mock authenticated user
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: { id: 1, email: 'test@example.com', first_name: 'John', last_name: 'Doe' },
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText('Logout')).toBeInTheDocument()
  })

  it('allows user to logout', () => {
    const mockLogout = vi.fn()
    
    // Mock authenticated user with logout function
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: { id: 1, email: 'test@example.com', first_name: 'John', last_name: 'Doe' },
      login: vi.fn(),
      logout: mockLogout
    })

    renderWithProviders(<Header />)

    const logoutButton = screen.getByText('Logout')
    fireEvent.click(logoutButton)

    expect(mockLogout).toHaveBeenCalled()
  })

  it('navigates to different pages when links are clicked', () => {
    // Mock empty cart and no user
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    const homeLink = screen.getByText('Home')
    const productsLink = screen.getByText('Products')
    const cartLink = screen.getByText('Cart (0)')

    expect(homeLink.closest('a')).toHaveAttribute('href', '/')
    expect(productsLink.closest('a')).toHaveAttribute('href', '/products')
    expect(cartLink.closest('a')).toHaveAttribute('href', '/cart')
  })

  it('displays search bar', () => {
    // Mock empty cart and no user
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    expect(screen.getByPlaceholderText('Search products...')).toBeInTheDocument()
  })

  it('handles search input', () => {
    // Mock empty cart and no user
    mockUseCart.mockReturnValue({
      getItemCount: () => 0
    })
    mockUseAuth.mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn()
    })

    renderWithProviders(<Header />)

    const searchInput = screen.getByPlaceholderText('Search products...')
    fireEvent.change(searchInput, { target: { value: 'vintage dress' } })

    expect(searchInput).toHaveValue('vintage dress')
  })
})