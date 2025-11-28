"""
Main FastAPI application for vintage store backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from .config import settings
from .routers import products, auth, orders, users, uploads
from .storage import storage_service

# Initialize FastAPI app
app = FastAPI(title=settings.app_name, version=settings.app_version)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(users.router)
app.include_router(uploads.router)

# Image upload endpoint is tricky because it uses storage service directly and was in main.
# It's admin only. I should probably put it in products router or a separate uploads router.
# Given it's for products, products router makes sense, or a dedicated 'admin' router.
# Let's see where I put it... I didn't put it in products.py.
# I'll add it to products.py or creating a new routers/upload.py.
# Let's put it in products.py for now as it is "upload_product_images".

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Vintage Store API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
