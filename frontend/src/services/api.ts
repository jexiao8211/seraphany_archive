/**
 * API service for communicating with the backend
 */
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Product {
  id: number
  name: string
  description: string
  price: number
  category: string
  images: string[]
  is_available: boolean
}

export interface CartItem {
  id: number
  name: string
  price: number
  quantity: number
  image: string
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
}

// Product API functions
export const getProducts = async (params?: {
  page?: number
  limit?: number
  category?: string
  search?: string
}): Promise<Product[]> => {
  const response = await api.get('/products', { params })
  return response.data
}

export const getProduct = async (id: number): Promise<Product> => {
  const response = await api.get(`/products/${id}`)
  return response.data
}

// Auth API functions
export const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password })
  return response.data
}

export const register = async (userData: {
  email: string
  password: string
  first_name: string
  last_name: string
}) => {
  const response = await api.post('/auth/register', userData)
  return response.data
}

// Order API functions
export const createOrder = async (orderData: {
  items: Array<{ product_id: number; quantity: number }>
  shipping_address: {
    street: string
    city: string
    state: string
    zip_code: string
    country: string
  }
}) => {
  const response = await api.post('/orders', orderData)
  return response.data
}

export default api
