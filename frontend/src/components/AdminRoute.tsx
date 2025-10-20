/**
 * Admin Route Component - Protects admin-only routes
 */
import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

interface AdminRouteProps {
  children: React.ReactNode
}

const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (!user.is_admin) {
    return (
      <div className="error-container">
        <h2>Access Denied</h2>
        <p>You don't have permission to access this page.</p>
        <button onClick={() => window.history.back()} className="admin-cancel-button">
          Go Back
        </button>
      </div>
    )
  }

  return <>{children}</>
}

export default AdminRoute
