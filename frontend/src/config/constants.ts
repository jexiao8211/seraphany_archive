/**
 * Central configuration constants for the application
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Image Upload Configuration
export const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB in bytes
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
export const ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
export const MAX_FILES_PER_UPLOAD = 10

// Pagination
export const DEFAULT_PAGE_SIZE = 100
export const PRODUCTS_PER_PAGE = 12

// UI Configuration
export const TOAST_DURATION = 3000 // 3 seconds
export const DEBOUNCE_DELAY = 300 // 300ms for search

// File Upload Paths
export const UPLOAD_PATHS = {
  PRODUCTS: '/uploads/products/',
} as const

// Environment
export const IS_DEVELOPMENT = import.meta.env.DEV
export const IS_PRODUCTION = import.meta.env.PROD
