/**
 * ProductDetailPage - Full product detail view with image gallery and related products
 */
import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProduct } from '../services/api'
import { useCart } from '../contexts/CartContext'
import { useToast } from '../contexts/ToastContext'
import { useFirstImageUrl } from '../hooks/useImageUrl'
import ImageGallery from '../components/ImageGallery'
import RelatedProducts from '../components/RelatedProducts'
import type { Product } from '../types'

const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { addItem } = useCart()
  const { showSuccess, showError } = useToast()

  const productId = id ? parseInt(id, 10) : null

  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => getProduct(productId!),
    enabled: !!productId,
  })

  const handleAddToCart = (product: Product) => {
    if (!product.is_available) {
      showError('This product is currently out of stock')
      return
    }

    addItem({
      id: product.id,
      name: product.name,
      price: product.price,
      image: useFirstImageUrl(product.images),
    })
    showSuccess('Added to cart!')
  }

  const handleBackToProducts = () => {
    navigate('/products')
  }

  if (isLoading) {
    return (
      <div className="product-detail-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading product details...</p>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="product-detail-page">
        <div className="error-container">
          <h2>Product Not Found</h2>
          <p>The product you're looking for doesn't exist or has been removed.</p>
          <button
            onClick={handleBackToProducts}
            className="btn btn-primary"
          >
            Back to Products
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="product-detail-page">
      <div className="product-detail-container">
        {/* Main Product Content */}
        <div className="product-content">
          {/* Image Gallery */}
          <div className="product-images">
            <ImageGallery product={product} />
          </div>

          {/* Product Information */}
          <div className="product-info">
            <div className="product-brand">{product.category.toUpperCase()}</div>
            <h1 className="product-name">{product.name}</h1>
            <div className="product-price">${product.price.toFixed(2)} USD</div>
            
            <div className="product-shipping">
              Shipping calculated at checkout.
            </div>

            {!product.is_available && (
              <div className="product-sold-out-badge">Sold out</div>
            )}

            <div className="product-actions">
              <button
                onClick={() => handleAddToCart(product)}
                disabled={!product.is_available}
                className={`add-to-cart-btn ${!product.is_available ? 'disabled' : ''}`}
              >
                {product.is_available ? 'Add to cart' : 'Out of Stock'}
              </button>
            </div>

            <div className="product-description">
              <p>{product.description}</p>
            </div>
          </div>
        </div>

        {/* Related Products */}
        <RelatedProducts currentProduct={product} />
      </div>
    </div>
  )
}

export default ProductDetailPage
