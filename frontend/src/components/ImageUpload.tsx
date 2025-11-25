/**
 * ImageUpload Component - Drag and drop file upload with preview and image reordering
 */
import React, { useState, useRef, useCallback } from 'react'
import { uploadProductImages } from '../services/api'
import { MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES, MAX_FILES_PER_UPLOAD } from '../config/constants'
import { useImageUrl } from '../hooks/useImageUrl'

interface ImageUploadProps {
  onImagesChange: (imagePaths: string[]) => void
  existingImages?: string[]
  maxFiles?: number
  className?: string
}

interface UploadedFile {
  file: File
  preview: string
  uploading: boolean
  error?: string
}

const ImageUpload: React.FC<ImageUploadProps> = ({
  onImagesChange,
  existingImages = [],
  maxFiles = MAX_FILES_PER_UPLOAD,
  className = ''
}) => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null)
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Handle drag events
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  // Handle file selection
  const handleFiles = useCallback((files: File[]) => {
    const validFiles: File[] = []
    const errors: string[] = []

    files.forEach(file => {
      // Validate file type
      if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
        errors.push(`${file.name}: Invalid file type. Only JPG, PNG, and WebP are allowed.`)
        return
      }

      // Validate file size
      if (file.size > MAX_FILE_SIZE) {
        errors.push(`${file.name}: File too large. Maximum size is ${MAX_FILE_SIZE / (1024 * 1024)}MB.`)
        return
      }

      validFiles.push(file)
    })

    if (validFiles.length === 0) {
      alert(errors.join('\n'))
      return
    }

    if (errors.length > 0) {
      alert(errors.join('\n'))
    }

    // Check total file limit using functional update to get current state
    setUploadedFiles(prev => {
      const totalFiles = prev.length + validFiles.length
      if (totalFiles > maxFiles) {
        alert(`Maximum ${maxFiles} files allowed.`)
        return prev
      }

      // Create preview objects
      const newFiles: UploadedFile[] = validFiles.map(file => ({
        file,
        preview: URL.createObjectURL(file),
        uploading: false
      }))

      return [...prev, ...newFiles]
    })
  }, [maxFiles])

  const handleFileDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    // Only handle file drops (not image reordering)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files))
    }
  }, [handleFiles])

  // Handle file input change
  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFiles(Array.from(e.target.files))
    }
  }

  // Remove file from list
  const removeFile = (index: number) => {
    setUploadedFiles(prev => {
      const newFiles = prev.filter((_, i) => i !== index)
      return newFiles
    })
  }

  // Remove existing image
  const removeExistingImage = (index: number) => {
    const newExistingImages = existingImages.filter((_, i) => i !== index)
    onImagesChange(newExistingImages)
  }

  // Handle drag start for reordering
  const handleDragStart = (index: number) => {
    setDraggedIndex(index)
  }

  // Handle drag over for reordering
  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault()
    e.stopPropagation()
    if (draggedIndex !== null && draggedIndex !== index) {
      setDragOverIndex(index)
    }
  }

  // Handle drag leave for reordering
  const handleDragLeave = () => {
    setDragOverIndex(null)
  }

  // Handle drop for reordering
  const handleImageReorderDrop = (e: React.DragEvent, dropIndex: number) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (draggedIndex === null || draggedIndex === dropIndex) {
      setDraggedIndex(null)
      setDragOverIndex(null)
      return
    }

    const newImages = [...existingImages]
    const draggedImage = newImages[draggedIndex]
    
    // Remove the dragged item
    newImages.splice(draggedIndex, 1)
    
    // Insert at new position
    newImages.splice(dropIndex, 0, draggedImage)
    
    onImagesChange(newImages)
    setDraggedIndex(null)
    setDragOverIndex(null)
  }

  // Handle drag end for reordering
  const handleDragEnd = () => {
    setDraggedIndex(null)
    setDragOverIndex(null)
  }

  // Upload files
  const uploadFiles = async () => {
    if (uploadedFiles.length === 0) {
      onImagesChange([...existingImages])
      return
    }

    setUploading(true)
    try {
      const filesToUpload = uploadedFiles.map(uf => uf.file)
      const response = await uploadProductImages(filesToUpload)
      
      // Combine existing images with new uploads
      const allImages = [...existingImages, ...response.uploaded_paths]
      onImagesChange(allImages)
      
      // Clear uploaded files
      setUploadedFiles([])
      
      if (response.errors && response.errors.length > 0) {
        alert(`Some uploads failed:\n${response.errors.join('\n')}`)
      }
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  // Trigger file input
  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className={`image-upload ${className}`}>
      <div className="image-upload-section">
        <h3 className="image-upload-title">Product Images</h3>
        
        {/* Existing Images */}
        {existingImages.length > 0 && (
          <div className="existing-images">
            <h4>Current Images (drag to reorder):</h4>
            <div className="image-preview-grid">
              {existingImages.map((imagePath, index) => (
                <div
                  key={index}
                  className={`image-preview-item ${draggedIndex === index ? 'dragging' : ''} ${dragOverIndex === index ? 'drag-over' : ''}`}
                  draggable
                  onDragStart={() => handleDragStart(index)}
                  onDragOver={(e) => handleDragOver(e, index)}
                  onDragLeave={handleDragLeave}
                  onDrop={(e) => handleImageReorderDrop(e, index)}
                  onDragEnd={handleDragEnd}
                >
                  <div className="drag-handle" title="Drag to reorder">
                    ⋮⋮
                  </div>
                  <img 
                    src={useImageUrl(imagePath)}
                    alt={`Product ${index + 1}`}
                    className="image-preview"
                    draggable={false}
                  />
                  <button
                    type="button"
                    onClick={() => removeExistingImage(index)}
                    className="remove-image-btn"
                    title="Remove image"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Upload Area */}
        <div
          className={`upload-area ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleFileDrop}
        >
          <div className="upload-content">
            <div className="upload-icon">📁</div>
            <p className="upload-text">
              Drag and drop images here, or{' '}
              <button
                type="button"
                onClick={triggerFileInput}
                className="upload-link"
              >
                browse files
              </button>
            </p>
            <p className="upload-hint">
              Supports JPG, PNG, WebP up to 5MB each
            </p>
          </div>
        </div>

        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/jpeg,image/jpg,image/png,image/webp"
          onChange={handleFileInputChange}
          className="hidden-file-input"
        />

        {/* Uploaded Files Preview */}
        {uploadedFiles.length > 0 && (
          <div className="uploaded-files">
            <h4>Files to Upload:</h4>
            <div className="image-preview-grid">
              {uploadedFiles.map((uploadedFile, index) => (
                <div key={index} className="image-preview-item">
                  <img 
                    src={uploadedFile.preview}
                    alt={`Upload ${index + 1}`}
                    className="image-preview"
                  />
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="remove-image-btn"
                    title="Remove file"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Upload Button */}
        {uploadedFiles.length > 0 && (
          <div className="upload-actions">
            <button
              type="button"
              onClick={uploadFiles}
              disabled={uploading}
              className="upload-button"
            >
              {uploading ? 'Uploading...' : `Upload ${uploadedFiles.length} file(s)`}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default ImageUpload
