"""
Uploads router - handles file uploads for product images
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List

from ..storage import storage_service
from ..dependencies import get_admin_user
from ..schemas import ImageUploadResponse, UserResponse

router = APIRouter(prefix="/upload", tags=["Uploads"])


@router.post("/product-images", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_product_images(
    files: List[UploadFile] = File(...),
    current_user: UserResponse = Depends(get_admin_user)
):
    """
    Upload product images (admin only).
    Accepts multiple image files with validation.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
    
    uploaded_paths: List[str] = []
    errors: List[str] = []
    
    for file in files:
        try:
            # Read file content
            content = await file.read()
            
            # Validate file
            is_valid, error_msg = storage_service.validate_image_file(
                file.filename or "unknown",
                len(content)
            )
            
            if not is_valid:
                errors.append(f"{file.filename}: {error_msg}")
                continue
            
            # Save file
            url_path = storage_service.save_image(content, file.filename or "image.jpg", "products")
            uploaded_paths.append(url_path)
            
        except Exception as e:
            errors.append(f"{file.filename}: Upload failed - {str(e)}")
    
    if errors and not uploaded_paths:
        # All uploads failed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"All uploads failed: {'; '.join(errors)}"
        )
    
    return ImageUploadResponse(
        uploaded_paths=uploaded_paths,
        errors=errors,
        message=f"Successfully uploaded {len(uploaded_paths)} file(s)"
    )

