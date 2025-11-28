"""
Main FastAPI application for vintage store backend.
Clean, modular architecture using routers for endpoint organization.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routers import (
    auth_router,
    products_router,
    orders_router,
    uploads_router,
    users_router,
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for Seraphany Archive vintage clothing store"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(uploads_router)
app.include_router(users_router)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "message": "Vintage Store API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
