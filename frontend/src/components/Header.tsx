/**
 * Header component with navigation
 * Desktop: Announcement bar, icon row, nav links row
 * Mobile: Hamburger menu, logo, search/cart icons
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
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isSearchExpanded, setIsSearchExpanded] = useState(false)
  const searchRef = useRef<HTMLDivElement>(null)
  const mobileMenuRef = useRef<HTMLDivElement>(null)

  const handleLogout = () => {
    logout()
    setIsMobileMenuOpen(false)
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
      setIsSearchExpanded(false)
    }
  }

  const handleSearchClose = () => {
    setIsSearchOpen(false)
  }

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen)
  }

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false)
  }

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsSearchOpen(false)
        setIsSearchExpanded(false)
      }
      if (mobileMenuRef.current && !mobileMenuRef.current.contains(event.target as Node)) {
        setIsMobileMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Close mobile menu on route change
  useEffect(() => {
    setIsMobileMenuOpen(false)
  }, [navigate])

  return (
    <header className="header">
      {/* Main Header */}
      <div className="header-main">
        <div className="header-container">
          {/* Mobile Menu Button */}
          <button 
            className="header-mobile-menu-btn"
            onClick={toggleMobileMenu}
            aria-label="Menu"
            aria-expanded={isMobileMenuOpen}
          >
            <span className={`hamburger ${isMobileMenuOpen ? 'open' : ''}`}>
              <span></span>
              <span></span>
              <span></span>
            </span>
          </button>

          {/* Left - Search (Desktop) */}
          <div className="header-left">
            <div className="header-search-wrapper" ref={searchRef}>
              <button 
                className="header-icon-btn"
                onClick={() => setIsSearchExpanded(!isSearchExpanded)}
                aria-label="Search"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="m21 21-4.35-4.35"/>
                </svg>
              </button>
              {isSearchExpanded && (
                <form onSubmit={handleSearchSubmit} className="header-search-form">
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={handleSearchChange}
                    onFocus={() => searchQuery.length > 0 && setIsSearchOpen(true)}
                    className="header-search-input"
                    autoFocus
                  />
                </form>
              )}
              <SearchDropdown
                searchQuery={searchQuery}
                isOpen={isSearchOpen}
                onClose={handleSearchClose}
              />
            </div>
          </div>

          {/* Center - Logo */}
          <Link to="/" className="header-logo">
            <img 
              src="/logo.png" 
              alt="Seraphany Archive" 
              className="header-logo-image"
            />
          </Link>

          {/* Right - Icons */}
          <div className="header-right">
            {/* Mobile Search Icon */}
            <button 
              className="header-icon-btn header-mobile-search"
              onClick={() => setIsSearchExpanded(!isSearchExpanded)}
              aria-label="Search"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
            </button>

            {/* Login Icon (Desktop) */}
            {user ? (
              <button
                onClick={handleLogout}
                className="header-icon-btn header-desktop-only"
                aria-label="Log out"
                title="Log out"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16,17 21,12 16,7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
              </button>
            ) : (
              <Link to="/login" className="header-icon-btn header-desktop-only" aria-label="Log in">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </Link>
            )}

            {/* Cart Icon */}
            <Link to="/cart" className="header-icon-btn header-cart-btn" aria-label="Cart">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                <line x1="3" y1="6" x2="21" y2="6"/>
                <path d="M16 10a4 4 0 0 1-8 0"/>
              </svg>
              {getItemCount() > 0 && (
                <span className="header-cart-badge">{getItemCount()}</span>
              )}
            </Link>
          </div>
        </div>

        {/* Mobile Search Bar (when expanded) */}
        {isSearchExpanded && (
          <div className="header-mobile-search-bar" ref={searchRef}>
            <form onSubmit={handleSearchSubmit} className="header-search-form-mobile">
              <input
                type="text"
                placeholder="Search..."
                value={searchQuery}
                onChange={handleSearchChange}
                className="header-search-input-mobile"
                autoFocus
              />
              <button type="button" onClick={() => setIsSearchExpanded(false)} className="header-search-close">
                ✕
              </button>
            </form>
            <SearchDropdown
              searchQuery={searchQuery}
              isOpen={isSearchOpen}
              onClose={handleSearchClose}
            />
          </div>
        )}
      </div>

      {/* Desktop Navigation Links */}
      <nav className="header-nav-desktop">
        <div className="header-nav-links">
          <Link to="/products" className="header-nav-link">Shop</Link>
          <Link to="/rentals" className="header-nav-link">Rentals</Link>
          <Link to="/appointments" className="header-nav-link">Showroom</Link>
          <Link to="/about" className="header-nav-link">About</Link>
          {user && (
            <Link to="/orders" className="header-nav-link">Orders</Link>
          )}
          {user?.is_admin && (
            <Link to="/admin/products" className="header-nav-link">Admin</Link>
          )}
        </div>
      </nav>

      {/* Mobile Menu Dropdown */}
      <div 
        ref={mobileMenuRef}
        className={`header-mobile-menu ${isMobileMenuOpen ? 'open' : ''}`}
      >
        <nav className="mobile-menu-nav">
          <Link to="/products" className="mobile-menu-link" onClick={closeMobileMenu}>
            Shop
          </Link>
          <Link to="/rentals" className="mobile-menu-link" onClick={closeMobileMenu}>
            Rentals
          </Link>
          <Link to="/appointments" className="mobile-menu-link" onClick={closeMobileMenu}>
            Showroom Appointments
          </Link>
          <Link to="/about" className="mobile-menu-link" onClick={closeMobileMenu}>
            About
          </Link>
          
          <div className="mobile-menu-divider"></div>
          
          {user ? (
            <>
              <Link to="/orders" className="mobile-menu-link" onClick={closeMobileMenu}>
                Orders
              </Link>
              {user.is_admin && (
                <Link to="/admin/products" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Admin
                </Link>
              )}
              <button onClick={handleLogout} className="mobile-menu-link mobile-menu-button">
                Log out
              </button>
            </>
          ) : (
            <Link to="/login" className="mobile-menu-link" onClick={closeMobileMenu}>
              Log in
            </Link>
          )}
        </nav>
      </div>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div className="header-overlay" onClick={closeMobileMenu}></div>
      )}
    </header>
  )
}

export default Header
