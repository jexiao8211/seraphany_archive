/**
 * API service for communicating with the backend
 */
import axios from 'axios'
import type { Product, User, ShippingAddress, LoginCredentials, RegisterData, AuthToken } from '../types'
import { authStorage } from '../utils/auth'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include JWT token
api.interceptors.request.use(
  (config) => {
    const token = authStorage.getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle 401 errors (token expired)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token is invalid or expired
      authStorage.clearAuth()
      // Optionally redirect to login
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// Re-export types for convenience
export type { Product, User, ShippingAddress, LoginCredentials, RegisterData, AuthToken } from '../types'

// Product API functions
export const getProducts = async (params?: {
  page?: number
  limit?: number
  category?: string
  search?: string
}): Promise<Product[]> => {
  const response = await api.get('/products', { params })
  // Backend returns { items: [...], total, page, pages }
  // Extract just the items array
  return response.data.items || response.data
}

export const getProduct = async (id: number): Promise<Product> => {
  const response = await api.get(`/products/${id}`)
  return response.data
}

// Auth API functions
export const login = async (credentials: LoginCredentials): Promise<AuthToken> => {
  const response = await api.post('/auth/login', credentials)
  return response.data
}

export const register = async (userData: RegisterData): Promise<User> => {
  const response = await api.post('/auth/register', userData)
  return response.data
}

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get('/auth/me')
  return response.data
}

export const logout = async (): Promise<void> => {
  try {
    await api.post('/auth/logout')
  } catch (error) {
    // Even if backend logout fails, clear local storage
    console.error('Logout error:', error)
  }
}

// Order API functions
export const createOrder = async (orderData: {
  items: Array<{ product_id: number; quantity: number }>
  shipping_address: ShippingAddress
}) => {
  const response = await api.post('/orders', orderData)
  return response.data
}

export default api
