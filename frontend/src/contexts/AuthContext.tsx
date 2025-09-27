/**
 * Authentication context for managing user state
 */
import React, { createContext, useContext, useState, ReactNode } from 'react'
import { User } from '../services/api'

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  register: (userData: {
    email: string
    password: string
    first_name: string
    last_name: string
  }) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)

  const login = async (email: string, password: string) => {
    // Mock login - in real implementation, this would call the API
    const mockUser: User = {
      id: 1,
      email,
      first_name: 'John',
      last_name: 'Doe'
    }
    setUser(mockUser)
  }

  const logout = () => {
    setUser(null)
  }

  const register = async (userData: {
    email: string
    password: string
    first_name: string
    last_name: string
  }) => {
    // Mock registration - in real implementation, this would call the API
    const mockUser: User = {
      id: 1,
      email: userData.email,
      first_name: userData.first_name,
      last_name: userData.last_name
    }
    setUser(mockUser)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
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
