/**
 * ImageGallery component for product detail pages
 * Features: main image display, thumbnail navigation, arrow controls, keyboard navigation
 * On mobile: carousel mode with swipe support
 * On desktop: stacked vertical gallery
 */
import React, { useState, useEffect, useRef } from 'react'
import { getFirstImageUrl } from '../hooks/useImageUrl'
import type { Product } from '../types'

interface ImageGalleryProps {
  product: Product
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ product }) => {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isMobile, setIsMobile] = useState(false)
  const carouselRef = useRef<HTMLDivElement>(null)
  const touchStartX = useRef<number | null>(null)
  const touchEndX = useRef<number | null>(null)

  // Get images array from product
  const images = product.images || []
  const hasImages = images.length > 0

  // Detect mobile viewport
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Handle touch events for swipe
  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX
  }

  const handleTouchMove = (e: React.TouchEvent) => {
    touchEndX.current = e.touches[0].clientX
  }

  const handleTouchEnd = () => {
    if (!touchStartX.current || !touchEndX.current) return

    const distance = touchStartX.current - touchEndX.current
    const minSwipeDistance = 50

    if (distance > minSwipeDistance && currentIndex < images.length - 1) {
      // Swipe left - next image
      setCurrentIndex(currentIndex + 1)
    } else if (distance < -minSwipeDistance && currentIndex > 0) {
      // Swipe right - previous image
      setCurrentIndex(currentIndex - 1)
    }

    touchStartX.current = null
    touchEndX.current = null
  }

  const goToNext = () => {
    setCurrentIndex((prev) => (prev < images.length - 1 ? prev + 1 : 0))
  }

  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : images.length - 1))
  }

  const goToSlide = (index: number) => {
    setCurrentIndex(index)
  }

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft' && currentIndex > 0) {
        setCurrentIndex(currentIndex - 1)
      } else if (e.key === 'ArrowRight' && currentIndex < images.length - 1) {
        setCurrentIndex(currentIndex + 1)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [currentIndex, images.length])

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

  // Mobile: Carousel mode
  if (isMobile) {
    return (
      <div className="image-gallery image-gallery-carousel">
        <div
          ref={carouselRef}
          className="carousel-container"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          <div
            className="carousel-track"
            style={{
              transform: `translateX(-${currentIndex * 100}%)`,
            }}
          >
            {images.map((image, index) => (
              <div key={index} className="carousel-slide">
                <div className="main-image-container">
                  <img
                    src={getFirstImageUrl([image])}
                    alt={`${product.name} - Image ${index + 1}`}
                    className="main-image"
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Navigation Arrows */}
          {images.length > 1 && (
            <>
              <button
                className="carousel-arrow carousel-arrow-left"
                onClick={goToPrevious}
                aria-label="Previous image"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M15 18l-6-6 6-6"/>
                </svg>
              </button>
              <button
                className="carousel-arrow carousel-arrow-right"
                onClick={goToNext}
                aria-label="Next image"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
            </>
          )}

          {/* Dots Indicator */}
          {images.length > 1 && (
            <div className="carousel-dots">
              {images.map((_, index) => (
                <button
                  key={index}
                  className={`carousel-dot ${index === currentIndex ? 'active' : ''}`}
                  onClick={() => goToSlide(index)}
                  aria-label={`Go to image ${index + 1}`}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    )
  }

  // Desktop: Stacked vertical gallery
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
