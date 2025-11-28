/**
 * Order Details Page - Display detailed information about a specific order
 */
import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getOrder, cancelOrder } from '../services/api'
import { useToast } from '../contexts/ToastContext'
import type { OrderItem } from '../types'

const OrderDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { showError, showSuccess } = useToast()
  const orderId = parseInt(id || '0', 10)

  const { data: order, isLoading, error } = useQuery({
    queryKey: ['order', orderId],
    queryFn: () => getOrder(orderId),
    enabled: !!orderId
  })

  const cancelOrderMutation = useMutation({
    mutationFn: () => cancelOrder(orderId),
    onSuccess: () => {
      showSuccess('Order cancelled successfully')
      // Refetch the order to get updated status
      queryClient.invalidateQueries({ queryKey: ['order', orderId] })
    },
    onError: (error) => {
      console.error('Failed to cancel order:', error)
      showError('Failed to cancel order. Please try again.')
    }
  })

  const handleCancelOrder = () => {
    if (!window.confirm('Are you sure you want to cancel this order?')) {
      return
    }
    cancelOrderMutation.mutate()
  }

  const handleBackToOrders = () => {
    navigate('/orders')
  }

  const handleContinueShopping = () => {
    navigate('/products')
  }

  if (isLoading) {
    return (
      <div className="order-details-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading order details...</p>
        </div>
      </div>
    )
  }

  if (error || !order) {
    return (
      <div className="order-details-page">
        <div className="error-container">
          <h2>Order not found</h2>
          <p>The order you're looking for doesn't exist or you don't have permission to view it.</p>
          <button onClick={handleBackToOrders} className="order-back-button">
            Back to Orders
          </button>
        </div>
      </div>
    )
  }

  const canCancel = order.status === 'PENDING' || order.status === 'CONFIRMED'

  return (
    <div className="order-details-page">
      <div className="order-details-header">
        <div className="order-details-title-section">
          <h1 className="order-details-title">Order #{order.id}</h1>
          <p className="order-details-date">
            Placed on {new Date(order.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="order-details-actions">
          <button 
            onClick={handleBackToOrders}
            className="order-back-button"
          >
            Back to Orders
          </button>
          {canCancel && (
            <button 
              onClick={handleCancelOrder}
              disabled={cancelOrderMutation.isPending}
              className="order-cancel-button"
            >
              {cancelOrderMutation.isPending ? 'Cancelling...' : 'Cancel Order'}
            </button>
          )}
        </div>
      </div>

      <div className="order-details-content">
        {/* Order Status */}
        <div className="order-status-section">
          <h2 className="order-section-title">Order Status</h2>
          <div className="order-status-info">
            <span className={`order-status-badge ${order.status.toLowerCase()}`}>
              {order.status}
            </span>
            <p className="order-status-description">
              {order.status === 'PENDING' && 'Your order is being processed.'}
              {order.status === 'CONFIRMED' && 'Your order has been confirmed and is being prepared.'}
              {order.status === 'SHIPPED' && 'Your order has been shipped and is on its way.'}
              {order.status === 'DELIVERED' && 'Your order has been delivered.'}
              {order.status === 'CANCELLED' && 'Your order has been cancelled.'}
            </p>
          </div>
        </div>

        {/* Order Items */}
        <div className="order-items-section">
          <h2 className="order-section-title">Items Ordered</h2>
          <div className="order-items-list">
            {order.items.map((item: OrderItem, index: number) => (
              <div key={index} className="order-item-detail">
                <div className="order-item-info">
                  <h3 className="order-item-name">{item.product_name}</h3>
                  <p className="order-item-price">${item.price.toFixed(2)} each</p>
                </div>
                <div className="order-item-quantity">
                  <span>Qty: {item.quantity}</span>
                </div>
                <div className="order-item-total">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="order-summary-section">
          <h2 className="order-section-title">Order Summary</h2>
          <div className="order-summary-details">
            <div className="order-summary-line">
              <span>Subtotal</span>
              <span>${order.total_amount.toFixed(2)}</span>
            </div>
            <div className="order-summary-line">
              <span>Shipping</span>
              <span>Free</span>
            </div>
            <div className="order-summary-line">
              <span>Tax</span>
              <span>Included</span>
            </div>
            <div className="order-summary-divider">
              <div className="order-summary-total">
                <span>Total</span>
                <span>${order.total_amount.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Shipping Address */}
        <div className="order-shipping-section">
          <h2 className="order-section-title">Shipping Address</h2>
          <div className="shipping-address-details">
            <p>{order.shipping_address.street}</p>
            <p>
              {order.shipping_address.city}, {order.shipping_address.state} {order.shipping_address.zip_code}
            </p>
            <p>{order.shipping_address.country}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="order-details-actions-bottom">
          <button 
            onClick={handleBackToOrders}
            className="order-action-button secondary"
          >
            Back to Orders
          </button>
          <button 
            onClick={handleContinueShopping}
            className="order-action-button primary"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  )
}

export default OrderDetailsPage
