/**
 * Tests for ProductList component
 * Following TDD approach - tests written before implementation
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import ProductList from '../components/ProductList'
import * as api from '../services/api'

// Mock the API
vi.mock('../services/api', () => ({
  getProducts: vi.fn()
}))

// Mock the cart context
const mockUseCart = vi.fn()
vi.mock('../contexts/CartContext', () => ({
  useCart: () => mockUseCart()
}))

const renderWithProviders = (component: React.ReactElement) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  })

  return render(
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        {component}
      </QueryClientProvider>
    </BrowserRouter>
  )
}

describe('ProductList', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockUseCart.mockReturnValue({
      addItem: vi.fn()
    })
  })

  it('renders loading state', () => {
    vi.mocked(api.getProducts).mockImplementation(() => new Promise(() => {})) // Never resolves

    renderWithProviders(<ProductList />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders error state', async () => {
    vi.mocked(api.getProducts).mockRejectedValue(new Error('API Error'))

    renderWithProviders(<ProductList />)

    await waitFor(() => {
      expect(screen.getByText('Error loading products')).toBeInTheDocument()
    })
  })

  it('renders products when loaded', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Vintage Chanel Dress',
        description: 'Beautiful vintage Chanel dress',
        price: 1500.00,
        category: 'dresses',
        images: ['image1.jpg'],
        is_available: true
      },
      {
        id: 2,
        name: 'Vintage Hermes Bag',
        description: 'Classic Hermes handbag',
        price: 2500.00,
        category: 'bags',
        images: ['image2.jpg'],
        is_available: true
      }
    ]

    vi.mocked(api.getProducts).mockResolvedValue(mockProducts)

    renderWithProviders(<ProductList />)

    await waitFor(() => {
      expect(screen.getByText('Vintage Chanel Dress')).toBeInTheDocument()
      expect(screen.getByText('Vintage Hermes Bag')).toBeInTheDocument()
    })
  })

  it('filters products by category', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Vintage Chanel Dress',
        description: 'Beautiful vintage Chanel dress',
        price: 1500.00,
        category: 'dresses',
        images: ['image1.jpg'],
        is_available: true
      },
      {
        id: 2,
        name: 'Vintage Hermes Bag',
        description: 'Classic Hermes handbag',
        price: 2500.00,
        category: 'bags',
        images: ['image2.jpg'],
        is_available: true
      }
    ]

    vi.mocked(api.getProducts).mockResolvedValue(mockProducts)

    renderWithProviders(<ProductList />)

    // Wait for products to load
    await waitFor(() => {
      expect(screen.getByText('Vintage Chanel Dress')).toBeInTheDocument()
    })

    // Filter by dresses category
    const categoryFilter = screen.getByLabelText('Category')
    fireEvent.change(categoryFilter, { target: { value: 'dresses' } })

    // The API should be called again with the filter
    await waitFor(() => {
      expect(api.getProducts).toHaveBeenCalledWith({ category: 'dresses', search: '' })
    })
  })

  it('searches products by name', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Vintage Chanel Dress',
        description: 'Beautiful vintage Chanel dress',
        price: 1500.00,
        category: 'dresses',
        images: ['image1.jpg'],
        is_available: true
      },
      {
        id: 2,
        name: 'Vintage Hermes Bag',
        description: 'Classic Hermes handbag',
        price: 2500.00,
        category: 'bags',
        images: ['image2.jpg'],
        is_available: true
      }
    ]

    vi.mocked(api.getProducts).mockResolvedValue(mockProducts)

    renderWithProviders(<ProductList />)

    // Wait for products to load
    await waitFor(() => {
      expect(screen.getByText('Vintage Chanel Dress')).toBeInTheDocument()
    })

    // Search for "Chanel"
    const searchInput = screen.getByPlaceholderText('Search products...')
    fireEvent.change(searchInput, { target: { value: 'Chanel' } })

    // The API should be called again with the search term
    await waitFor(() => {
      expect(api.getProducts).toHaveBeenCalledWith({ category: '', search: 'Chanel' })
    })
  })

  it('adds product to cart when add to cart button is clicked', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Vintage Chanel Dress',
        description: 'Beautiful vintage Chanel dress',
        price: 1500.00,
        category: 'dresses',
        images: ['image1.jpg'],
        is_available: true
      }
    ]

    vi.mocked(api.getProducts).mockResolvedValue(mockProducts)

    const mockAddItem = vi.fn()
    mockUseCart.mockReturnValue({
      addItem: mockAddItem
    })

    renderWithProviders(<ProductList />)

    await waitFor(() => {
      expect(screen.getByText('Vintage Chanel Dress')).toBeInTheDocument()
    })

    const addToCartButton = screen.getByText('Add to Cart')
    fireEvent.click(addToCartButton)

    expect(mockAddItem).toHaveBeenCalledWith({
      id: 1,
      name: 'Vintage Chanel Dress',
      price: 1500.00,
      image: 'image1.jpg'
    })
  })
})