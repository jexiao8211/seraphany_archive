/**
 * Authentication utility functions
 * Handles token storage and retrieval
 */
import type { User } from '../types'

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'

export const authStorage = {
  // Token management
  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token)
  },

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
  },

  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY)
  },

  // User data management
  setUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  },

  getUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY)
    if (!userStr) return null
    try {
      return JSON.parse(userStr) as User
    } catch {
      return null
    }
  },

  removeUser(): void {
    localStorage.removeItem(USER_KEY)
  },

  // Clear all auth data
  clearAuth(): void {
    this.removeToken()
    this.removeUser()
  },
}
