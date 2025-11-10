/**
 * About page - Information about the vintage store
 */
import React from 'react'

const AboutPage: React.FC = () => {
  return (
    <div className="about-page">
      <div className="about-container">
        <h1 className="about-title">About Us</h1>
        <div className="about-content">
          <section className="about-intro">
            <h2 className="about-section-title">Our Story</h2>
            <p className="about-description">
              Welcome to Vintage Store, your destination for authentic vintage treasures.
              We are passionate about curating unique pieces from the past and bringing
              them to new homes where they can be appreciated and loved once again.
            </p>
          </section>

          <section className="about-mission">
            <h2 className="about-section-title">Our Mission</h2>
            <p className="about-description">
              Our mission is to preserve the beauty and craftsmanship of vintage items
              while making them accessible to collectors, enthusiasts, and anyone who
              appreciates the timeless appeal of well-made pieces from eras gone by.
            </p>
          </section>

          <section className="about-values">
            <h2 className="about-section-title">What We Value</h2>
            <div className="about-values-list">
              <div className="about-value">
                <h3 className="about-value-title">Authenticity</h3>
                <p className="about-value-description">
                  Every item is carefully authenticated and verified for its vintage status
                </p>
              </div>
              <div className="about-value">
                <h3 className="about-value-title">Quality</h3>
                <p className="about-value-description">
                  We only offer items that meet our high standards for condition and quality
                </p>
              </div>
              <div className="about-value">
                <h3 className="about-value-title">Customer Service</h3>
                <p className="about-value-description">
                  Your satisfaction is our priority, and we're here to help you find the perfect piece
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

export default AboutPage

