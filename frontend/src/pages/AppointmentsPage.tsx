/**
 * Appointments page - Showroom appointment booking information
 */
import React from 'react'

const AppointmentsPage: React.FC = () => {
  return (
    <div className="appointments-page">
      <div className="appointments-container">
        <h1 className="appointments-title">Showroom Appointments</h1>
        <div className="appointments-content">
          <section className="appointments-intro">
            <p className="appointments-description">
              Visit our showroom to see our vintage collection in person.
              Schedule an appointment for a personalized shopping experience.
            </p>
          </section>

          <section className="appointments-info">
            <h2 className="appointments-section-title">Why Schedule an Appointment?</h2>
            <div className="appointments-benefits">
              <div className="appointments-benefit">
                <h3 className="appointments-benefit-title">Personalized Service</h3>
                <p className="appointments-benefit-description">
                  Get one-on-one assistance from our vintage experts
                </p>
              </div>
              <div className="appointments-benefit">
                <h3 className="appointments-benefit-title">Exclusive Access</h3>
                <p className="appointments-benefit-description">
                  View items not yet listed online and special collections
                </p>
              </div>
              <div className="appointments-benefit">
                <h3 className="appointments-benefit-title">Expert Guidance</h3>
                <p className="appointments-benefit-description">
                  Learn about the history and authenticity of each piece
                </p>
              </div>
            </div>
          </section>

          <section className="appointments-cta">
            <h2 className="appointments-section-title">Schedule Your Visit</h2>
            <p className="appointments-cta-text">
              Contact us to book your showroom appointment. We're here to help you
              find the perfect vintage piece.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}

export default AppointmentsPage

