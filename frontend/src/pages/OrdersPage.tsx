/**
 * Orders Page - Display user's order history
 */
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getUserOrders } from '../services/api'
import type { Order } from '../types'

const OrdersPage: React.FC = () => {
  const navigate = useNavigate()

  const { data: orders = [], isLoading, error } = useQuery({
    queryKey: ['user-orders'],
    queryFn: getUserOrders
  })

  const handleViewOrder = (orderId: number) => {
    navigate(`/orders/${orderId}`)
  }

  const handleContinueShopping = () => {
    navigate('/products')
  }

  if (isLoading) {
    return (
      <div className="orders-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading your orders...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="orders-page">
        <div className="error-container">
          <h2>Error loading orders</h2>
          <p>Please try again later.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="orders-page">
      <div className="orders-header">
        <h1 className="orders-title">Your Orders</h1>
        <button 
          onClick={handleContinueShopping}
          className="orders-continue-button"
        >
          Continue Shopping
        </button>
      </div>

      {orders.length === 0 ? (
        <div className="orders-empty">
          <h2>No orders yet</h2>
          <p>You haven't placed any orders yet. Start shopping to see your orders here.</p>
          <button 
            onClick={handleContinueShopping}
            className="orders-continue-button"
          >
            Start Shopping
          </button>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order: Order) => (
            <div key={order.id} className="order-card">
              <div className="order-card-header">
                <div className="order-info">
                  <h3 className="order-number">Order #{order.id}</h3>
                  <p className="order-date">
                    Placed on {new Date(order.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="order-status-container">
                  <span className={`order-status ${order.status.toLowerCase()}`}>
                    {order.status}
                  </span>
                </div>
              </div>

              <div className="order-card-content">
                <div className="order-items-preview">
                  <h4>Items ({order.items.length})</h4>
                  <div className="order-items-list">
                    {order.items.slice(0, 3).map((item, index) => (
                      <div key={index} className="order-item-preview">
                        <span className="order-item-name">{item.product_name}</span>
                        <span className="order-item-quantity">Qty: {item.quantity}</span>
                        <span className="order-item-price">${item.price.toFixed(2)}</span>
                      </div>
                    ))}
                    {order.items.length > 3 && (
                      <div className="order-item-more">
                        +{order.items.length - 3} more items
                      </div>
                    )}
                  </div>
                </div>

                <div className="order-total">
                  <span className="order-total-label">Total:</span>
                  <span className="order-total-amount">${order.total_amount.toFixed(2)}</span>
                </div>
              </div>

              <div className="order-card-actions">
                <button 
                  onClick={() => handleViewOrder(order.id)}
                  className="order-view-button"
                >
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default OrdersPage
