/**
 * SearchDropdown component - Shows product search results with thumbnails
 * Similar to pomchili.com search functionality
 */
import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProducts } from '../services/api'
import { getFirstImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

interface SearchDropdownProps {
  searchQuery: string
  isOpen: boolean
  onClose: () => void
}

const SearchDropdown: React.FC<SearchDropdownProps> = ({
  searchQuery,
  isOpen,
  onClose,
}) => {
  const { data: products, isLoading } = useQuery({
    queryKey: ['search-products', searchQuery],
    queryFn: () => getProducts({ search: searchQuery, limit: 8 }),
    enabled: searchQuery.length > 0 && isOpen,
  })

  if (!isOpen || searchQuery.length === 0) {
    return null
  }

  return (
    <div className="search-dropdown" onClick={(e) => e.stopPropagation()}>
      {isLoading ? (
        <div className="search-dropdown-loading">
          <p>Searching...</p>
        </div>
      ) : products && products.length > 0 ? (
        <>
          <div className="search-dropdown-results">
            {products.map((product: Product) => (
              <Link
                key={product.id}
                to={`/products/${product.id}`}
                className="search-dropdown-item"
                onClick={onClose}
              >
                <div className="search-dropdown-item-image">
                  <img
                    src={getFirstImageUrl(product.images) || '/placeholder.jpg'}
                    alt={product.name}
                  />
                </div>
                <div className="search-dropdown-item-info">
                  <h4 className="search-dropdown-item-name">{product.name}</h4>
                  <p className="search-dropdown-item-price">
                    ${product.price.toFixed(2)}
                  </p>
                </div>
              </Link>
            ))}
          </div>
          {products.length >= 8 && (
            <div className="search-dropdown-footer">
              <Link
                to={`/products?search=${encodeURIComponent(searchQuery)}`}
                className="search-dropdown-view-all"
                onClick={onClose}
              >
                View all results for "{searchQuery}"
              </Link>
            </div>
          )}
        </>
      ) : (
        <div className="search-dropdown-empty">
          <p>No products found</p>
        </div>
      )}
    </div>
  )
}

export default SearchDropdown

