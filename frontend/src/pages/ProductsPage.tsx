/**
 * Products page - Display all products with filtering and search
 */
import React from 'react'
import { useSearchParams } from 'react-router-dom'
import ProductList from '../components/ProductList'

const ProductsPage: React.FC = () => {
  const [searchParams] = useSearchParams()
  const searchQuery = searchParams.get('search') || ''

  return (
    <div className="products-page">
      <h1 className="products-title">
        {searchQuery ? `Search Results for "${searchQuery}"` : 'Our Products'}
      </h1>
      <ProductList searchQuery={searchQuery} />
    </div>
  )
}

export default ProductsPage

