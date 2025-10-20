/**
 * Order Confirmation Page - Display order details after successful checkout
 */
import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getOrder } from '../services/api'
import type { Order } from '../types'

const OrderConfirmationPage: React.FC = () => {
  const { orderId } = useParams<{ orderId: string }>()
  const navigate = useNavigate()
  const orderIdNum = parseInt(orderId || '0', 10)

  const { data: order, isLoading, error } = useQuery({
    queryKey: ['order', orderIdNum],
    queryFn: () => getOrder(orderIdNum),
    enabled: !!orderIdNum
  })

  const handleViewOrders = () => {
    navigate('/orders')
  }

  const handleContinueShopping = () => {
    navigate('/products')
  }

  if (isLoading) {
    return (
      <div className="order-confirmation-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading order details...</p>
        </div>
      </div>
    )
  }

  if (error || !order) {
    return (
      <div className="order-confirmation-page">
        <div className="error-container">
          <h2>Order not found</h2>
          <p>The order you're looking for doesn't exist.</p>
          <button onClick={() => navigate('/orders')} className="checkout-continue-button">
            View Your Orders
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="order-confirmation-page">
      <div className="order-confirmation-header">
        <h1 className="order-confirmation-title">Order Confirmed!</h1>
        <p className="order-confirmation-subtitle">
          Thank you for your purchase. Your order has been placed successfully.
        </p>
      </div>

      <div className="order-confirmation-content">
        {/* Order Details */}
        <div className="order-details">
          <h2 className="order-details-title">Order Details</h2>
          
          <div className="order-info">
            <div className="order-info-item">
              <span className="order-info-label">Order Number:</span>
              <span className="order-info-value">#{order.id}</span>
            </div>
            <div className="order-info-item">
              <span className="order-info-label">Order Date:</span>
              <span className="order-info-value">
                {new Date(order.created_at).toLocaleDateString()}
              </span>
            </div>
            <div className="order-info-item">
              <span className="order-info-label">Status:</span>
              <span className={`order-status ${order.status.toLowerCase()}`}>
                {order.status}
              </span>
            </div>
            <div className="order-info-item">
              <span className="order-info-label">Total:</span>
              <span className="order-info-value order-total">
                ${order.total_amount.toFixed(2)}
              </span>
            </div>
          </div>
        </div>

        {/* Order Items */}
        <div className="order-items">
          <h2 className="order-items-title">Items Ordered</h2>
          
          <div className="order-items-list">
            {order.items.map((item, index) => (
              <div key={index} className="order-item">
                <div className="order-item-details">
                  <h3 className="order-item-name">{item.product_name}</h3>
                  <p className="order-item-price">${item.price.toFixed(2)} each</p>
                  <p className="order-item-quantity">Quantity: {item.quantity}</p>
                </div>
                <div className="order-item-total">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Shipping Address */}
        <div className="order-shipping">
          <h2 className="order-shipping-title">Shipping Address</h2>
          
          <div className="shipping-address">
            <p>{order.shipping_address.street}</p>
            <p>
              {order.shipping_address.city}, {order.shipping_address.state} {order.shipping_address.zip_code}
            </p>
            <p>{order.shipping_address.country}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="order-confirmation-actions">
          <button 
            onClick={handleViewOrders}
            className="order-confirmation-button primary"
          >
            View Order History
          </button>
          <button 
            onClick={handleContinueShopping}
            className="order-confirmation-button secondary"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  )
}

export default OrderConfirmationPage
