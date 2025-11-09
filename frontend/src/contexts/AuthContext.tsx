/**
 * Authentication context for managing user state
 */
import React, { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import type { User, RegisterData } from '../types'
import * as api from '../services/api'
import { authStorage } from '../utils/auth'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  register: (userData: RegisterData) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Auto-login on app load if token exists
  useEffect(() => {
    const initAuth = async () => {
      const token = authStorage.getToken()
      const savedUser = authStorage.getUser()

      if (token && savedUser) {
        // Try to verify token is still valid by fetching current user
        try {
          const currentUser = await api.getCurrentUser()
          setUser(currentUser)
          authStorage.setUser(currentUser) // Update saved user data
        } catch (error) {
          // Token is invalid, clear auth data
          authStorage.clearAuth()
          setUser(null)
        }
      }
      setIsLoading(false)
    }

    initAuth()
  }, [])

  const login = async (email: string, password: string) => {
    try {
      // Call login API
      const tokenData = await api.login({ email, password })
      
      // Store token
      authStorage.setToken(tokenData.access_token)
      
      // Fetch user data
      const userData = await api.getCurrentUser()
      
      // Update state and storage
      setUser(userData)
      authStorage.setUser(userData)
    } catch (error: any) {
      // Clear any partial auth data
      authStorage.clearAuth()
      throw new Error(error.response?.data?.detail || 'Login failed')
    }
  }

  const logout = async () => {
    try {
      // Call logout API (optional, backend may not need it)
      await api.logout()
    } catch (error) {
      console.error('Logout API error:', error)
    } finally {
      // Always clear local auth data
      authStorage.clearAuth()
      setUser(null)
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      // Call register API
      await api.register(userData)
      
      // After registration, log the user in automatically
      await login(userData.email, userData.password)
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        logout,
        register,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
