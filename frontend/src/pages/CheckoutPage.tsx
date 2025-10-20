/**
 * Checkout Page - Complete order with shipping address
 */
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useCart } from '../contexts/CartContext'
import { useAuth } from '../contexts/AuthContext'
import { createOrder } from '../services/api'
import type { ShippingAddress } from '../types'

interface ShippingFormData {
  street: string
  city: string
  state: string
  zip_code: string
  country: string
}

const CheckoutPage: React.FC = () => {
  const navigate = useNavigate()
  const { items, getTotalPrice, clearCart } = useCart()
  const { user } = useAuth()
  
  const [formData, setFormData] = useState<ShippingFormData>({
    street: '',
    city: '',
    state: '',
    zip_code: '',
    country: ''
  })
  const [errors, setErrors] = useState<Partial<ShippingFormData>>({})

  const createOrderMutation = useMutation({
    mutationFn: createOrder,
    onSuccess: (order) => {
      clearCart()
      navigate(`/order-confirmation/${order.id}`)
    },
    onError: (error) => {
      console.error('Failed to create order:', error)
      alert('Failed to create order. Please try again.')
    }
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    
    // Clear error when user starts typing
    if (errors[name as keyof ShippingFormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<ShippingFormData> = {}

    if (!formData.street.trim()) {
      newErrors.street = 'Street address is required'
    }

    if (!formData.city.trim()) {
      newErrors.city = 'City is required'
    }

    if (!formData.state.trim()) {
      newErrors.state = 'State is required'
    }

    if (!formData.zip_code.trim()) {
      newErrors.zip_code = 'ZIP code is required'
    }

    if (!formData.country.trim()) {
      newErrors.country = 'Country is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    const orderData = {
      items: items.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      })),
      shipping_address: formData as ShippingAddress
    }

    createOrderMutation.mutate(orderData)
  }

  const handleCancel = () => {
    navigate('/cart')
  }

  if (!user) {
    navigate('/login')
    return null
  }

  if (items.length === 0) {
    return (
      <div className="checkout-page">
        <div className="checkout-empty">
          <h1>Your cart is empty</h1>
          <p>Add some items to your cart before checking out.</p>
          <button 
            onClick={() => navigate('/products')}
            className="checkout-continue-button"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="checkout-page">
      <div className="checkout-header">
        <h1 className="checkout-title">Checkout</h1>
        <button 
          onClick={handleCancel}
          className="checkout-cancel-button"
        >
          Back to Cart
        </button>
      </div>

      <div className="checkout-layout">
        {/* Order Summary */}
        <div className="checkout-summary">
          <h2 className="checkout-summary-title">Order Summary</h2>
          
          <div className="checkout-items">
            {items.map((item) => (
              <div key={item.id} className="checkout-item">
                <img
                  src={item.image || 'https://via.placeholder.com/60'}
                  alt={item.name}
                  className="checkout-item-image"
                />
                <div className="checkout-item-details">
                  <h3 className="checkout-item-name">{item.name}</h3>
                  <p className="checkout-item-price">${item.price.toFixed(2)}</p>
                  <p className="checkout-item-quantity">Qty: {item.quantity}</p>
                </div>
                <div className="checkout-item-total">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>

          <div className="checkout-totals">
            <div className="checkout-total-line">
              <span>Subtotal</span>
              <span>${getTotalPrice().toFixed(2)}</span>
            </div>
            <div className="checkout-total-line">
              <span>Shipping</span>
              <span>Calculated at checkout</span>
            </div>
            <div className="checkout-total-line">
              <span>Tax</span>
              <span>Calculated at checkout</span>
            </div>
            <div className="checkout-total-divider">
              <div className="checkout-total-final">
                <span>Total</span>
                <span>${getTotalPrice().toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Shipping Form */}
        <div className="checkout-form-container">
          <form onSubmit={handleSubmit} className="checkout-form">
            <h2 className="checkout-form-title">Shipping Address</h2>
            
            <div className="form-group">
              <label htmlFor="street" className="form-label">
                Street Address *
              </label>
              <input
                type="text"
                id="street"
                name="street"
                value={formData.street}
                onChange={handleInputChange}
                className={`form-input ${errors.street ? 'error' : ''}`}
                placeholder="123 Main Street"
              />
              {errors.street && <span className="form-error">{errors.street}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="city" className="form-label">
                  City *
                </label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  className={`form-input ${errors.city ? 'error' : ''}`}
                  placeholder="New York"
                />
                {errors.city && <span className="form-error">{errors.city}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="state" className="form-label">
                  State *
                </label>
                <input
                  type="text"
                  id="state"
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className={`form-input ${errors.state ? 'error' : ''}`}
                  placeholder="NY"
                />
                {errors.state && <span className="form-error">{errors.state}</span>}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="zip_code" className="form-label">
                  ZIP Code *
                </label>
                <input
                  type="text"
                  id="zip_code"
                  name="zip_code"
                  value={formData.zip_code}
                  onChange={handleInputChange}
                  className={`form-input ${errors.zip_code ? 'error' : ''}`}
                  placeholder="10001"
                />
                {errors.zip_code && <span className="form-error">{errors.zip_code}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="country" className="form-label">
                  Country *
                </label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleInputChange}
                  className={`form-input ${errors.country ? 'error' : ''}`}
                  placeholder="United States"
                />
                {errors.country && <span className="form-error">{errors.country}</span>}
              </div>
            </div>

            <div className="checkout-actions">
              <button
                type="button"
                onClick={handleCancel}
                className="checkout-button cancel-button"
              >
                Back to Cart
              </button>
              <button
                type="submit"
                disabled={createOrderMutation.isPending}
                className="checkout-button submit-button"
              >
                {createOrderMutation.isPending ? 'Placing Order...' : 'Place Order'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default CheckoutPage
