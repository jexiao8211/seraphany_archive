/**
 * Products page - Display all products with filtering and search
 */
import React from 'react'
import ProductList from '../components/ProductList'

const ProductsPage: React.FC = () => {
  return (
    <div className="products-page">
      <h1 className="products-title">Our Products</h1>
      <ProductList />
    </div>
  )
}

export default ProductsPage

