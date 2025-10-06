/**
 * Header component with navigation and cart
 */
import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'
import { useAuth } from '../contexts/AuthContext'

const Header: React.FC = () => {
  const { getItemCount } = useCart()
  const { user, logout } = useAuth()
  const [searchQuery, setSearchQuery] = useState('')

  const handleLogout = () => {
    logout()
  }

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-content">
          {/* Logo */}
          <Link to="/" className="header-logo">
            Vintage Store
          </Link>

          {/* Navigation */}
          <nav className="header-nav">
            <Link to="/" className="header-nav-link">
              Home
            </Link>
            <Link to="/products" className="header-nav-link">
              Products
            </Link>
            <Link to="/cart" className="header-nav-link">
              Cart ({getItemCount()})
            </Link>
          </nav>

          {/* Search Bar */}
          <div className="header-search">
            <input
              type="text"
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="header-search-input"
            />
          </div>

          {/* Auth Section */}
          <div className="header-auth">
            {user ? (
              <>
                <span className="header-user-name">
                  {user.first_name} {user.last_name}
                </span>
                <button
                  onClick={handleLogout}
                  className="header-auth-button"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="header-auth-link">
                  Login
                </Link>
                <Link to="/register" className="header-auth-link">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
