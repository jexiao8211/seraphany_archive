"""
Storage module for handling file uploads and management.
Supports local storage with future cloud migration capability.
"""
import os
import uuid
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import shutil
from .config import get_upload_dir, get_max_file_size, get_allowed_file_types


class StorageService:
    """Storage service for handling file operations"""
    
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = Path(base_path or get_upload_dir())
        self.products_path = self.base_path / "products"
        
        # Ensure directories exist
        self.products_path.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, file_content: bytes, filename: str, folder: str = "products") -> str:
        """
        Save an image file and return the relative URL path.
        
        Args:
            file_content: The file content as bytes
            filename: Original filename
            folder: Storage folder (default: "products")
            
        Returns:
            Relative URL path (e.g., "/uploads/products/xyz.jpg")
        """
        # Generate unique filename
        file_ext = Path(filename).suffix.lower()
        unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_ext}"
        
        # Determine storage path
        if folder == "products":
            storage_path = self.products_path / unique_name
        else:
            storage_path = self.base_path / folder / unique_name
            storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(storage_path, 'wb') as f:
            f.write(file_content)
        
        # Return relative URL path
        return f"/uploads/{folder}/{unique_name}"
    
    def delete_image(self, url_path: str) -> bool:
        """
        Delete an image file by its URL path.
        
        Args:
            url_path: The URL path (e.g., "/uploads/products/xyz.jpg")
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # Convert URL path to file path
            if url_path.startswith("/uploads/"):
                file_path = self.base_path / url_path[9:]  # Remove "/uploads/" prefix
                if file_path.exists():
                    file_path.unlink()
                    return True
            return False
        except Exception:
            return False
    
    def get_file_size(self, url_path: str) -> Optional[int]:
        """
        Get file size in bytes.
        
        Args:
            url_path: The URL path
            
        Returns:
            File size in bytes or None if not found
        """
        try:
            if url_path.startswith("/uploads/"):
                file_path = self.base_path / url_path[9:]
                if file_path.exists():
                    return file_path.stat().st_size
        except Exception:
            pass
        return None
    
    def validate_image_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """
        Validate image file before saving.
        
        Args:
            filename: Original filename
            file_size: File size in bytes
            
        Returns:
            (is_valid, error_message)
        """
        # Check file extension
        allowed_extensions = get_allowed_file_types()
        file_ext = Path(filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        
        # Check file size
        max_size_bytes = get_max_file_size()
        if file_size > max_size_bytes:
            max_size_mb = max_size_bytes // (1024 * 1024)
            return False, f"File too large. Maximum size: {max_size_mb}MB"
        
        return True, ""


# Global storage service instance
storage_service = StorageService()
