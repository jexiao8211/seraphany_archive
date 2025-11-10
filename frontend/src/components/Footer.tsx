/**
 * Footer component
 * Simplified layout matching Pomchili.com
 */
import React, { useState } from 'react'

const Footer: React.FC = () => {
  const [email, setEmail] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement newsletter subscription
    console.log('Newsletter subscription:', email)
    setEmail('')
  }

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-title">Subscribe to our newsletter</h3>
            <form onSubmit={handleSubmit} className="footer-newsletter">
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="footer-newsletter-input"
                required
              />
              <button type="submit" className="footer-newsletter-button">
                Subscribe
              </button>
            </form>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-copyright">
            &copy; {new Date().getFullYear()}, Vintage Store
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

