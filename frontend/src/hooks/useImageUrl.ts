/**
 * Utility functions for constructing image URLs with API base URL
 * Note: These are NOT React hooks - they're pure functions.
 * Named without "use" prefix to avoid confusion with React hooks.
 */
import { API_BASE_URL } from '../config/constants'

/**
 * Constructs a full image URL from a relative path
 * @param imagePath - Relative image path (e.g., "/uploads/products/image.jpg")
 * @returns Full image URL or empty string if no path provided
 */
export const getImageUrl = (imagePath?: string): string => {
  if (!imagePath) return ''
  return `${API_BASE_URL}${imagePath}`
}

/**
 * Constructs image URLs for multiple images
 * @param imagePaths - Array of relative image paths
 * @returns Array of full image URLs
 */
export const getImageUrls = (imagePaths: string[]): string[] => {
  return imagePaths.map(path => getImageUrl(path))
}

/**
 * Gets the first image URL from an array of image paths
 * @param imagePaths - Array of relative image paths
 * @returns First image URL or empty string
 */
export const getFirstImageUrl = (imagePaths: string[]): string => {
  return getImageUrl(imagePaths[0])
}

