/**
 * ImageGallery component for product detail pages
 * Features: main image display, thumbnail navigation, arrow controls, keyboard navigation
 */
import React from 'react'
import { getFirstImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

interface ImageGalleryProps {
  product: Product
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ product }) => {
  // Get images array from product
  const images = product.images || []
  const hasImages = images.length > 0

  // If no images, show placeholder
  if (!hasImages) {
    return (
      <div className="image-gallery">
        <div className="main-image-container">
          <img
            src="/placeholder.jpg"
            alt={product.name}
            className="main-image"
          />
        </div>
      </div>
    )
  }

  // Display all images stacked vertically
  return (
    <div className="image-gallery">
      {images.map((image, index) => (
        <div 
          key={index} 
          className="main-image-container"
        >
          <img
            src={getFirstImageUrl([image])}
            alt={`${product.name} - Image ${index + 1}`}
            className="main-image"
          />
        </div>
      ))}
    </div>
  )
}

export default ImageGallery
