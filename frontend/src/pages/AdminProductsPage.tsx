/**
 * Admin Products Page - Display all products with admin actions
 */
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProducts, deleteProduct } from '../services/api'
import { useToast } from '../contexts/ToastContext'
import type { Product } from '../types'
import { getFirstImageUrl } from '../hooks/useImageUrl'

const AdminProductsPage: React.FC = () => {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [deleteLoading, setDeleteLoading] = useState<number | null>(null)
  const { showSuccess, showError } = useToast()

  // Fetch products
  const { data: products = [], isLoading, error, refetch } = useQuery({
    queryKey: ['admin-products', searchTerm, categoryFilter],
    queryFn: () => getProducts({ search: searchTerm, category: categoryFilter || undefined })
  })

  const handleDelete = async (productId: number) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return
    }

    setDeleteLoading(productId)
    try {
      await deleteProduct(productId)
      refetch() // Refresh the list
      showSuccess('Product deleted successfully')
    } catch (error) {
      console.error('Failed to delete product:', error)
      showError('Failed to delete product. Please try again.')
    } finally {
      setDeleteLoading(null)
    }
  }

  const handleEdit = (productId: number) => {
    navigate(`/admin/products/${productId}/edit`)
  }

  const handleCreate = () => {
    navigate('/admin/products/new')
  }

  if (isLoading) {
    return (
      <div className="admin-products-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading products...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="admin-products-page">
        <div className="error-container">
          <h2>Error loading products</h2>
          <p>Please try again later.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-products-page">
      <div className="admin-header">
        <h1 className="admin-title">Manage Products</h1>
        <button 
          onClick={handleCreate}
          className="admin-create-button"
        >
          Add New Product
        </button>
      </div>

      {/* Search and Filter Controls */}
      <div className="admin-controls">
        <div className="admin-search">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="admin-search-input"
          />
        </div>
        <div className="admin-filter">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="admin-filter-select"
          >
            <option value="">All Categories</option>
            <option value="accessories">Accessories</option>
            <option value="bags">Bags</option>
            <option value="coats">Coats</option>
            <option value="dresses">Dresses</option>
            <option value="jackets">Jackets</option>
            <option value="pants">Pants</option>
            <option value="shoes">Shoes</option>
            <option value="shorts">Shorts</option>
            <option value="skirts">Skirts</option>
            <option value="tops">Tops</option>
          </select>
        </div>
      </div>

      {/* Products Table */}
      <div className="admin-products-table">
        {products.length === 0 ? (
          <div className="admin-empty">
            <p>No products found</p>
            <button onClick={handleCreate} className="admin-create-button">
              Add Your First Product
            </button>
          </div>
        ) : (
          <table className="products-table">
            <thead>
              <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Category</th>
                <th>Price</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product: Product) => (
                <tr key={product.id}>
                  <td>
                    <img
                      src={getFirstImageUrl(product.images) || 'https://via.placeholder.com/50'}
                      alt={product.name}
                      className="product-thumbnail"
                    />
                  </td>
                  <td>
                    <div className="product-info">
                      <h3 className="product-name">{product.name}</h3>
                      <p className="product-description">{product.description}</p>
                    </div>
                  </td>
                  <td>
                    <span className="product-category">{product.category}</span>
                  </td>
                  <td>
                    <span className="product-price">${product.price.toFixed(2)}</span>
                  </td>
                  <td>
                    <span className={`product-status ${product.is_available ? 'available' : 'unavailable'}`}>
                      {product.is_available ? 'Available' : 'Unavailable'}
                    </span>
                  </td>
                  <td>
                    <div className="product-actions">
                      <button
                        onClick={() => handleEdit(product.id)}
                        className="action-button edit-button"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(product.id)}
                        disabled={deleteLoading === product.id}
                        className="action-button delete-button"
                      >
                        {deleteLoading === product.id ? 'Deleting...' : 'Delete'}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default AdminProductsPage
