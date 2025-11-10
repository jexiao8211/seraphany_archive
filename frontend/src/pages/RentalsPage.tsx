/**
 * Rentals page - Display rental information and options
 */
import React from 'react'

const RentalsPage: React.FC = () => {
  return (
    <div className="rentals-page">
      <div className="rentals-container">
        <h1 className="rentals-title">Rentals</h1>
        <div className="rentals-content">
          <section className="rentals-intro">
            <p className="rentals-description">
              Looking to rent vintage items for your special event or photoshoot?
              We offer a curated selection of vintage pieces available for rental.
            </p>
          </section>

          <section className="rentals-info">
            <h2 className="rentals-section-title">How It Works</h2>
            <div className="rentals-steps">
              <div className="rentals-step">
                <h3 className="rentals-step-title">1. Browse Available Items</h3>
                <p className="rentals-step-description">
                  Explore our collection of rentable vintage items
                </p>
              </div>
              <div className="rentals-step">
                <h3 className="rentals-step-title">2. Contact Us</h3>
                <p className="rentals-step-description">
                  Reach out to discuss your rental needs and availability
                </p>
              </div>
              <div className="rentals-step">
                <h3 className="rentals-step-title">3. Pick Up & Return</h3>
                <p className="rentals-step-description">
                  Arrange pickup and return dates for your rental period
                </p>
              </div>
            </div>
          </section>

          <section className="rentals-cta">
            <h2 className="rentals-section-title">Interested in Renting?</h2>
            <p className="rentals-cta-text">
              Please contact us to discuss your rental needs and check availability.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}

export default RentalsPage

