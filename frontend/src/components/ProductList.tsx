/**
 * ProductList component for displaying and filtering products
 */
import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProducts } from '../services/api'
import { useCart } from '../contexts/CartContext'
import { useToast } from '../contexts/ToastContext'
import { useFirstImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

const ProductList: React.FC = () => {
  const [category, setCategory] = useState('')
  const [search, setSearch] = useState('')
  const { addItem } = useCart()
  const { showSuccess } = useToast()

  const { data: products, isLoading, error } = useQuery({
    queryKey: ['products', category, search],
    queryFn: () => getProducts({ category, search }),
  })

  const handleAddToCart = (e: React.MouseEvent, product: Product) => {
    e.preventDefault() // Prevent navigation when clicking Add to Cart
    e.stopPropagation()
    addItem({
      id: product.id,
      name: product.name,
      price: product.price,
      image: useFirstImageUrl(product.images),
    })
    showSuccess('Added to cart!')
  }

  if (isLoading) {
    return <div className="loading-state">Loading...</div>
  }

  if (error) {
    return <div className="error-state">Error loading products</div>
  }

  return (
    <div className="product-list-container">
      {/* Filters */}
      <div className="product-filters">
        <div className="filter-search">
          <input
            type="text"
            placeholder="Search products..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="filter-input"
          />
        </div>
        <div className="filter-category">
          <label htmlFor="category-filter" className="filter-label">
            Category
          </label>
          <select
            id="category-filter"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="filter-select"
            aria-label="Category"
          >
            <option value="">All Categories</option>
            <option value="dresses">Dresses</option>
            <option value="bags">Bags</option>
            <option value="shoes">Shoes</option>
            <option value="accessories">Accessories</option>
          </select>
        </div>
      </div>

      {/* Products Grid */}
      <div className="products-grid">
        {products?.map((product) => (
          <Link
            key={product.id}
            to={`/products/${product.id}`}
            className="product-card"
          >
            <div className="product-image-container">
              <img
                src={useFirstImageUrl(product.images) || '/placeholder.jpg'}
                alt={product.name}
                className="product-image"
              />
            </div>
            <div className="product-info">
              <h3 className="product-name">
                {product.name}
              </h3>
              <p className="product-description">
                {product.description}
              </p>
              <div className="product-footer">
                <span className="product-price">
                  ${product.price.toFixed(2)}
                </span>
                <button
                  onClick={(e) => handleAddToCart(e, product)}
                  className="add-to-cart-btn"
                >
                  Add to Cart
                </button>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {products?.length === 0 && (
        <div className="no-products">
          No products found matching your criteria.
        </div>
      )}
    </div>
  )
}

export default ProductList
