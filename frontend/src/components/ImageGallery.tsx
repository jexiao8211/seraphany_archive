/**
 * ImageGallery component for product detail pages
 * Features: main image display, thumbnail navigation, arrow controls, keyboard navigation
 */
import React, { useState, useEffect } from 'react'
import { useFirstImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

interface ImageGalleryProps {
  product: Product
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ product }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  
  // Get images array from product
  const images = product.images || []
  const hasImages = images.length > 0
  
  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft') {
        event.preventDefault()
        goToPrevious()
      } else if (event.key === 'ArrowRight') {
        event.preventDefault()
        goToNext()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [currentImageIndex, images.length])

  const goToNext = () => {
    if (images.length > 1) {
      setCurrentImageIndex((prev) => (prev + 1) % images.length)
    }
  }

  const goToPrevious = () => {
    if (images.length > 1) {
      setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length)
    }
  }

  const goToImage = (index: number) => {
    setCurrentImageIndex(index)
  }

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

  // If only one image, don't show navigation
  if (images.length === 1) {
    return (
      <div className="image-gallery">
        <div className="main-image-container">
          <img
            src={useFirstImageUrl(images)}
            alt={product.name}
            className="main-image"
          />
        </div>
      </div>
    )
  }

  return (
    <div className="image-gallery">
      {/* Main Image */}
      <div className="main-image-container">
        <img
          src={useFirstImageUrl([images[currentImageIndex]])}
          alt={`${product.name} - Image ${currentImageIndex + 1}`}
          className="main-image"
        />
        
        {/* Navigation Arrows */}
        <button
          className="nav-arrow nav-arrow-left"
          onClick={goToPrevious}
          aria-label="Previous image"
        >
          &#8249;
        </button>
        <button
          className="nav-arrow nav-arrow-right"
          onClick={goToNext}
          aria-label="Next image"
        >
          &#8250;
        </button>
      </div>

      {/* Thumbnail Strip */}
      <div className="thumbnail-strip">
        {images.map((image, index) => (
          <button
            key={index}
            className={`thumbnail ${index === currentImageIndex ? 'active' : ''}`}
            onClick={() => goToImage(index)}
            aria-label={`View image ${index + 1}`}
          >
            <img
              src={useFirstImageUrl([image])}
              alt={`${product.name} thumbnail ${index + 1}`}
            />
          </button>
        ))}
      </div>
    </div>
  )
}

export default ImageGallery
