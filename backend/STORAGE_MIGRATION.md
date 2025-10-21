# Storage Migration Guide

This document outlines how to migrate from local file storage to cloud storage (AWS S3, Cloudflare R2, etc.).

## Current Architecture

- Images stored in `backend/uploads/products/`
- Served via FastAPI StaticFiles at `/uploads/*`
- Frontend accesses via `${API_BASE_URL}/uploads/products/filename.jpg`
- Database stores relative paths in `products.images` JSON column

## Migration Steps

### 1. Choose Cloud Provider

**AWS S3:**
- Most popular, extensive features
- Good for production scale
- Higher costs for bandwidth

**Cloudflare R2:**
- S3-compatible API
- No egress fees
- Good performance with Cloudflare CDN

**Other options:**
- Google Cloud Storage
- Azure Blob Storage
- DigitalOcean Spaces

### 2. Update Storage Service

Replace `backend/app/storage.py` implementation:

```python
# Example for AWS S3
import boto3
from botocore.exceptions import ClientError

class S3StorageService:
    def __init__(self, bucket_name: str, region: str = 'us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region)
        self.bucket_name = bucket_name
    
    def save_image(self, file_content: bytes, filename: str, folder: str = "products") -> str:
        # Generate unique filename
        unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{Path(filename).suffix}"
        key = f"{folder}/{unique_name}"
        
        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=file_content,
            ContentType='image/jpeg'  # or detect from extension
        )
        
        return f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{key}"
    
    def delete_image(self, url_path: str) -> bool:
        try:
            # Extract key from URL
            key = url_path.split('/')[-2] + '/' + url_path.split('/')[-1]
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False
```

### 3. Environment Variables

Add to `.env`:
```bash
# S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=your-bucket-name
AWS_S3_REGION=us-east-1

# Or for Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your-bucket-name
```

### 4. Update Dependencies

Add cloud storage dependencies to `pyproject.toml`:

```toml
# For AWS S3
boto3 = "^1.26.0"

# For Cloudflare R2 (S3-compatible)
boto3 = "^1.26.0"
```

### 5. Migration Script

Create `backend/migrate_images.py`:

```python
"""
Script to migrate existing local images to cloud storage.
Run this once after setting up cloud storage.
"""
import os
import json
from pathlib import Path
from app.database import DatabaseService
from app.storage import storage_service  # Your new cloud storage service

def migrate_images():
    db = DatabaseService()
    
    # Get all products with images
    products = db.get_products(limit=1000)  # Adjust limit as needed
    
    for product in products['products']:
        if not product['images']:
            continue
            
        new_images = []
        for image_path in product['images']:
            if image_path.startswith('/uploads/'):
                # Local file - migrate to cloud
                local_path = f"uploads{image_path[8:]}"  # Remove /uploads prefix
                
                if os.path.exists(local_path):
                    with open(local_path, 'rb') as f:
                        content = f.read()
                    
                    # Upload to cloud
                    cloud_url = storage_service.save_image(content, os.path.basename(local_path))
                    new_images.append(cloud_url)
                    
                    # Optional: delete local file after successful upload
                    # os.remove(local_path)
                else:
                    print(f"Warning: Local file not found: {local_path}")
            else:
                # Already a cloud URL
                new_images.append(image_path)
        
        # Update product with new image URLs
        if new_images != product['images']:
            db.update_product(product['id'], {'images': new_images})
            print(f"Migrated images for product {product['id']}: {product['name']}")

if __name__ == "__main__":
    migrate_images()
```

### 6. Update Frontend (if needed)

The frontend should work without changes since it uses the same API endpoints. However, you might want to:

1. Update CORS settings for your cloud storage domain
2. Add CDN configuration for better performance
3. Update image optimization settings

### 7. Testing

1. Test image upload with new cloud storage
2. Verify existing images still load correctly
3. Test image deletion
4. Run migration script on a copy of production data first

### 8. Deployment

1. Deploy backend with new storage service
2. Run migration script
3. Update environment variables
4. Monitor for any issues

## Rollback Plan

If issues occur:

1. Revert to local storage service
2. Update environment variables
3. Restore from local file backups
4. Update database with local paths

## Cost Considerations

- **Local Storage**: Free but limited by server disk space
- **S3**: Pay for storage + bandwidth
- **R2**: Pay for storage only (no egress fees)
- **CDN**: Additional cost but better performance

Choose based on your traffic patterns and budget.
