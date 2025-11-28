/**
 * ProductList component for displaying and filtering products
 */
import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProducts } from '../services/api'
import { useImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

interface ProductListProps {
  searchQuery?: string
}

interface ProductCardProps {
  product: Product
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [hoveredImageIndex, setHoveredImageIndex] = useState(0)
  const imageUrls = product.images.map(img => useImageUrl(img))
  const hasMultipleImages = imageUrls.length > 1
  
  const getCurrentImage = () => {
    if (hasMultipleImages && hoveredImageIndex > 0) {
      return imageUrls[hoveredImageIndex] || imageUrls[0]
    }
    return imageUrls[0] || '/placeholder.jpg'
  }

  return (
    <div className="product-card-wrapper">
      <Link
        to={`/products/${product.id}`}
        className="product-card"
        onMouseEnter={() => {
          if (hasMultipleImages) {
            setHoveredImageIndex(1)
          }
        }}
        onMouseLeave={() => {
          setHoveredImageIndex(0)
        }}
      >
        <div className="product-image-container">
          <img
            src={getCurrentImage()}
            alt={product.name}
            className="product-image"
          />
          {!product.is_available && (
            <span className="product-sold-out">Sold out</span>
          )}
        </div>
      </Link>
      <div className="product-info">
        <div className="product-name">{product.name}</div>
        <div className="product-price">${product.price.toFixed(2)} usd</div>
      </div>
    </div>
  )
}

const ProductList: React.FC<ProductListProps> = ({ searchQuery = '' }) => {
  const [category, setCategory] = useState('')

  // Fetch all products to extract available categories
  const { data: allProducts } = useQuery({
    queryKey: ['products', 'all'],
    queryFn: () => getProducts(),
  })

  // Extract unique categories from products
  const availableCategories = React.useMemo(() => {
    if (!allProducts?.items) return []
    const categories = new Set<string>()
    allProducts.items.forEach(product => {
      if (product.category) {
        categories.add(product.category)
      }
    })
    return Array.from(categories).sort()
  }, [allProducts])

  // Fetch filtered products
  const { data: productsData, isLoading, error } = useQuery({
    queryKey: ['products', category, searchQuery],
    queryFn: () => getProducts({ category, search: searchQuery || undefined }),
  })

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
            {availableCategories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Products Grid */}
      <div className="products-grid">
        {productsData?.items.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>

      {productsData?.items.length === 0 && (
        <div className="no-products">
          No products found matching your criteria.
        </div>
      )}
    </div>
  )
}

export default ProductList
