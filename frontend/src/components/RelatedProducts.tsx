/**
 * RelatedProducts component for showing products from the same category
 */
import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProducts } from '../services/api'
import { useFirstImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

interface RelatedProductsProps {
  currentProduct: Product
}

const RelatedProducts: React.FC<RelatedProductsProps> = ({ currentProduct }) => {
  const { data: allProducts, isLoading } = useQuery({
    queryKey: ['products', currentProduct.category],
    queryFn: () => getProducts({ category: currentProduct.category }),
  })

  // Filter out current product and limit to 6 items
  const relatedProducts = allProducts
    ?.filter(product => product.id !== currentProduct.id && product.is_available)
    .slice(0, 6) || []

  if (isLoading) {
    return (
      <div className="related-products">
        <h3 className="related-products-title">Related Products</h3>
        <div className="loading">Loading related products...</div>
      </div>
    )
  }

  if (relatedProducts.length === 0) {
    return null
  }

  return (
    <div className="related-products">
      <h3 className="related-products-title">Related Products</h3>
      <div className="related-products-grid">
        {relatedProducts.map((product) => (
          <Link
            key={product.id}
            to={`/products/${product.id}`}
            className="related-product-card"
          >
            <div className="product-image-container">
              <img
                src={useFirstImageUrl(product.images) || '/placeholder.jpg'}
                alt={product.name}
                className="product-image"
              />
            </div>
            <div className="product-info">
              <h4 className="product-name">{product.name}</h4>
              <p className="product-price">${product.price.toFixed(2)}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default RelatedProducts
