/**
 * Cart page - Shopping cart with checkout functionality
 */
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'
import { useAuth } from '../contexts/AuthContext'

const CartPage: React.FC = () => {
  const { items, removeItem, updateQuantity, getTotalPrice } = useCart()
  const { user } = useAuth()
  const navigate = useNavigate()

  const handleCheckout = () => {
    if (!user) {
      navigate('/login')
      return
    }
    // TODO: Implement checkout flow
    alert('Checkout functionality coming soon!')
  }

  if (items.length === 0) {
    return (
      <div className="cart-page">
        <h1 className="cart-title">Shopping Cart</h1>
        <div className="cart-empty">
          <p className="cart-empty-text">Your cart is empty</p>
          <button
            onClick={() => navigate('/products')}
            className="cart-empty-button"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="cart-page">
      <h1 className="cart-title">Shopping Cart</h1>
      
      <div className="cart-layout">
        {/* Cart Items */}
        <div className="cart-items">
          {items.map((item) => (
            <div key={item.id} className="cart-item">
              <img
                src={item.image || 'https://via.placeholder.com/100'}
                alt={item.name}
                className="cart-item-image"
              />
              <div className="cart-item-details">
                <h3 className="cart-item-name">{item.name}</h3>
                <p className="cart-item-price">${item.price.toFixed(2)}</p>
              </div>
              <div className="cart-item-quantity">
                <button
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="cart-item-quantity-btn"
                >
                  -
                </button>
                <span className="cart-item-quantity-value">{item.quantity}</span>
                <button
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="cart-item-quantity-btn"
                >
                  +
                </button>
              </div>
              <div className="cart-item-actions">
                <p className="cart-item-total">
                  ${(item.price * item.quantity).toFixed(2)}
                </p>
                <button
                  onClick={() => removeItem(item.id)}
                  className="cart-item-remove"
                >
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary */}
        <div className="cart-summary">
          <h2 className="cart-summary-title">Order Summary</h2>
          <div className="cart-summary-line">
            <span>Subtotal</span>
            <span>${getTotalPrice().toFixed(2)}</span>
          </div>
          <div className="cart-summary-line">
            <span>Shipping</span>
            <span>Calculated at checkout</span>
          </div>
          <div className="cart-summary-line">
            <span>Tax</span>
            <span>Calculated at checkout</span>
          </div>
          <div className="cart-summary-divider">
            <div className="cart-summary-total">
              <span>Total</span>
              <span>${getTotalPrice().toFixed(2)}</span>
            </div>
          </div>
          <button
            onClick={handleCheckout}
            className="cart-summary-checkout"
          >
            Proceed to Checkout
          </button>
          <button
            onClick={() => navigate('/products')}
            className="cart-summary-continue"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  )
}

export default CartPage

