/**
 * Central configuration constants for the application
 */

// API Configuration
function getApiBaseUrl(): string {
  const envUrl = import.meta.env.VITE_API_BASE_URL
  
  // If no env var is set, use localhost for development
  if (!envUrl || typeof envUrl !== 'string' || envUrl.trim() === '') {
    if (import.meta.env.PROD) {
      console.error(
        '⚠️ VITE_API_BASE_URL is not set in production! Falling back to localhost:8000. ' +
        'This will cause CORS errors. Please set VITE_API_BASE_URL in your Railway environment variables.'
      )
    }
    return 'http://localhost:8000'
  }
  
  const trimmedUrl = envUrl.trim()
  
  // Ensure URL has a protocol
  if (!trimmedUrl.startsWith('http://') && !trimmedUrl.startsWith('https://')) {
    console.warn(
      `⚠️ VITE_API_BASE_URL is missing protocol. Adding https://. ` +
      `Current value: "${trimmedUrl}". ` +
      `Please set VITE_API_BASE_URL with full URL including protocol (e.g., https://backend.up.railway.app)`
    )
    return `https://${trimmedUrl}`
  }
  
  // Log the API URL in both dev and prod for debugging
  if (import.meta.env.DEV) {
    console.log('🔧 API Base URL (dev):', trimmedUrl)
  } else {
    // In production, log once to help debug deployment issues
    console.log('🔧 API Base URL (prod):', trimmedUrl)
  }
  
  return trimmedUrl
}

export const API_BASE_URL = getApiBaseUrl()

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
