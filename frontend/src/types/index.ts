/**
 * Shared TypeScript type definitions
 */

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  is_admin: boolean
}

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

export interface Order {
  id: number
  user_id: number
  items: OrderItem[]
  total_amount: number
  status: string
  shipping_address: ShippingAddress
  created_at: string
  updated_at: string
}

export interface OrderItem {
  product_id: number
  quantity: number
  price: number
  product_name: string
}

export interface ShippingAddress {
  street: string
  city: string
  state: string
  zip_code: string
  country: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
}

export interface AuthToken {
  access_token: string
  token_type: string
}

