/**
 * Home page - Landing page for the vintage store
 */
import React from 'react'
import { Link } from 'react-router-dom'

const HomePage: React.FC = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="home-hero">
        <div className="home-hero-container">
          <h1 className="home-hero-title">Welcome to Vintage Store</h1>
          <p className="home-hero-subtitle">
            Discover unique vintage treasures from the past
          </p>
          <Link to="/products" className="home-hero-cta">
            Shop Now
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="home-features">
        <div className="home-features-container">
          <h2 className="home-features-title">Why Choose Us</h2>
          <div className="home-features-grid">
            <div className="home-feature-card">
              <div className="home-feature-icon">🎨</div>
              <h3 className="home-feature-title">Curated Collection</h3>
              <p className="home-feature-description">
                Handpicked vintage items from around the world
              </p>
            </div>
            <div className="home-feature-card">
              <div className="home-feature-icon">✨</div>
              <h3 className="home-feature-title">Quality Guaranteed</h3>
              <p className="home-feature-description">
                Every item is carefully inspected for authenticity
              </p>
            </div>
            <div className="home-feature-card">
              <div className="home-feature-icon">🚚</div>
              <h3 className="home-feature-title">Fast Shipping</h3>
              <p className="home-feature-description">
                Quick and secure delivery to your doorstep
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="home-cta">
        <div className="home-cta-container">
          <h2 className="home-cta-title">Start Your Collection Today</h2>
          <p className="home-cta-subtitle">
            Browse our collection of authentic vintage items
          </p>
          <Link to="/products" className="home-cta-button">
            View All Products
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage

