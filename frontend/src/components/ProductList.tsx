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

interface ProductListProps {
  searchQuery?: string
}

const ProductList: React.FC<ProductListProps> = ({ searchQuery = '' }) => {
  const [category, setCategory] = useState('')
  const { addItem } = useCart()
  const { showSuccess } = useToast()

  const { data: products, isLoading, error } = useQuery({
    queryKey: ['products', category, searchQuery],
    queryFn: () => getProducts({ category, search: searchQuery || undefined }),
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
              {!product.is_available && (
                <span className="product-sold-out">Sold out</span>
              )}
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
