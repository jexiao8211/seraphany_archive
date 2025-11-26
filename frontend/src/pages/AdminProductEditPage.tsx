/**
 * Admin Product Edit Page - Form to edit existing products
 */
import React, { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getProduct, updateProduct } from '../services/api'
import { useToast } from '../contexts/ToastContext'
import ImageUpload from '../components/ImageUpload'

interface ProductFormData {
  name: string
  description: string
  price: string
  category: string
  images: string[]
}

const AdminProductEditPage: React.FC = () => {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { showSuccess, showError } = useToast()
  const { id } = useParams<{ id: string }>()
  const productId = parseInt(id || '0', 10)

  const [formData, setFormData] = useState<ProductFormData>({
    name: '',
    description: '',
    price: '',
    category: '',
    images: []
  })
  const [errors, setErrors] = useState<Partial<ProductFormData>>({})

  // Fetch product data
  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => getProduct(productId),
    enabled: !!productId
  })

  const updateProductMutation = useMutation({
    mutationFn: (data: Parameters<typeof updateProduct>[1]) => updateProduct(productId, data),
    onSuccess: (updatedProduct) => {
      // Update the specific product cache immediately
      queryClient.setQueryData(['product', productId], updatedProduct)
      
      // Invalidate all product-related queries to ensure consistency
      queryClient.invalidateQueries({ queryKey: ['product', productId] })
      queryClient.invalidateQueries({ queryKey: ['admin-products'] })
      queryClient.invalidateQueries({ queryKey: ['products'] })
      queryClient.invalidateQueries({ queryKey: ['search-products'] })
      
      showSuccess('Product updated successfully')
      navigate('/admin/products')
    },
    onError: (error) => {
      console.error('Failed to update product:', error)
      showError('Failed to update product. Please try again.')
    }
  })

  // Populate form when product data is loaded
  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name,
        description: product.description,
        price: product.price.toString(),
        category: product.category,
        images: product.images
      })
    }
  }, [product])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    
    // Clear error when user starts typing
    if (errors[name as keyof ProductFormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<ProductFormData> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Product name is required'
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Product description is required'
    }

    if (!formData.price.trim()) {
      newErrors.price = 'Price is required'
    } else {
      const price = parseFloat(formData.price)
      if (isNaN(price) || price <= 0) {
        newErrors.price = 'Price must be a positive number'
      }
    }

    if (!formData.category.trim()) {
      newErrors.category = 'Category is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    const productData = {
      name: formData.name.trim(),
      description: formData.description.trim(),
      price: parseFloat(formData.price),
      category: formData.category.trim(),
      images: formData.images
    }

    updateProductMutation.mutate(productData)
  }

  const handleCancel = () => {
    navigate('/admin/products')
  }

  if (isLoading) {
    return (
      <div className="admin-product-form-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading product...</p>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="admin-product-form-page">
        <div className="error-container">
          <h2>Product not found</h2>
          <p>The product you're looking for doesn't exist.</p>
          <button onClick={handleCancel} className="admin-cancel-button">
            Back to Products
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-product-form-page">
      <div className="admin-header">
        <h1 className="admin-title">Edit Product</h1>
        <button 
          onClick={handleCancel}
          className="admin-cancel-button"
        >
          Back to Products
        </button>
      </div>

      <form onSubmit={handleSubmit} className="admin-product-form">
        <div className="form-group">
          <label htmlFor="name" className="form-label">
            Product Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            className={`form-input ${errors.name ? 'error' : ''}`}
            placeholder="Enter product name"
          />
          {errors.name && <span className="form-error">{errors.name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="description" className="form-label">
            Description *
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            className={`form-textarea ${errors.description ? 'error' : ''}`}
            rows={4}
            placeholder="Enter product description"
          />
          {errors.description && <span className="form-error">{errors.description}</span>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="price" className="form-label">
              Price *
            </label>
            <input
              type="number"
              id="price"
              name="price"
              value={formData.price}
              onChange={handleInputChange}
              className={`form-input ${errors.price ? 'error' : ''}`}
              placeholder="0.00"
              step="0.01"
              min="0"
            />
            {errors.price && <span className="form-error">{errors.price}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="category" className="form-label">
              Category *
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              className={`form-select ${errors.category ? 'error' : ''}`}
            >
              <option value="">Select a category</option>
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
            {errors.category && <span className="form-error">{errors.category}</span>}
          </div>
        </div>

        <div className="form-group">
          <ImageUpload
            onImagesChange={(imagePaths) => setFormData(prev => ({ ...prev, images: imagePaths }))}
            existingImages={formData.images}
            maxFiles={10}
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={handleCancel}
            className="form-button cancel-button"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={updateProductMutation.isPending}
            className="form-button submit-button"
          >
            {updateProductMutation.isPending ? 'Updating...' : 'Update Product'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default AdminProductEditPage
