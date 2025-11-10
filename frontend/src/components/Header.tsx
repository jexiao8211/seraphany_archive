/**
 * Header component with navigation
 * Simplified layout matching Pomchili.com
 */
import React, { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useCart } from '../contexts/CartContext'
import SearchDropdown from './SearchDropdown'

const Header: React.FC = () => {
  const { user, logout } = useAuth()
  const { getItemCount } = useCart()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const searchRef = useRef<HTMLDivElement>(null)

  const handleLogout = () => {
    logout()
  }

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value)
    setIsSearchOpen(e.target.value.length > 0)
  }

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery)}`)
      setIsSearchOpen(false)
      setSearchQuery('')
    }
  }

  const handleSearchClose = () => {
    setIsSearchOpen(false)
  }

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsSearchOpen(false)
      }
    }

    if (isSearchOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isSearchOpen])

  return (
    <header className="header">
      {/* Main Navigation Bar - Logo and Nav Links */}
      <div className="header-main-nav">
        <div className="header-main-container">
          {/* Logo */}
          <Link to="/" className="header-logo">
            Vintage Store
          </Link>

          {/* Main Navigation */}
          <nav className="header-nav">
            <Link to="/products" className="header-nav-link">
              Shop
            </Link>
            <Link to="/rentals" className="header-nav-link">
              Rentals
            </Link>
            <Link to="/appointments" className="header-nav-link">
              Showroom Appointments
            </Link>
            <Link to="/about" className="header-nav-link">
              About
            </Link>
            
            {/* Search */}
            <div className="header-search-wrapper" ref={searchRef}>
              <form onSubmit={handleSearchSubmit} className="header-search-form">
                <input
                  type="text"
                  placeholder="Search"
                  value={searchQuery}
                  onChange={handleSearchChange}
                  onFocus={() => searchQuery.length > 0 && setIsSearchOpen(true)}
                  className="header-search-input"
                />
              </form>
              <SearchDropdown
                searchQuery={searchQuery}
                isOpen={isSearchOpen}
                onClose={handleSearchClose}
              />
            </div>

            {/* Cart */}
            <Link to="/cart" className="header-nav-link header-cart-link">
              Cart {getItemCount() > 0 && `(${getItemCount()})`}
            </Link>

            {/* Auth */}
            {user ? (
              <>
                <Link to="/orders" className="header-nav-link">
                  Orders
                </Link>
                <button
                  onClick={handleLogout}
                  className="header-nav-link header-logout-button"
                >
                  Log out
                </button>
              </>
            ) : (
              <Link to="/login" className="header-nav-link">
                Log in
              </Link>
            )}
            {user?.is_admin && (
              <Link to="/admin/products" className="header-nav-link admin-link">
                Admin
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
