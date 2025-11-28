"""
Products router - handles product CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from ..database import DatabaseService
from ..dependencies import get_database_service, get_admin_user
from ..schemas import (
    ProductCreate,
    ProductResponse,
    ProductListResponse,
    UserResponse,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
async def get_products(
    page: int = 1,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: DatabaseService = Depends(get_database_service)
):
    """Get products with optional filtering and pagination."""
    result = db.get_products(page=page, limit=limit, category=category, search=search)
    return result


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: DatabaseService = Depends(get_database_service)
):
    """Get a single product by ID."""
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user: UserResponse = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Create a new product (admin only)."""
    try:
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "images": product.images,
            "is_available": True
        }
        
        created_product = db.create_product(product_data)
        
        return ProductResponse(
            id=created_product["id"],
            name=created_product["name"],
            description=created_product["description"],
            price=created_product["price"],
            category=created_product["category"],
            images=created_product["images"],
            is_available=created_product["is_available"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductCreate,
    current_user: UserResponse = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Update a product (admin only)."""
    try:
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "images": product.images
        }
        
        updated_product = db.update_product(product_id, product_data)
        
        return ProductResponse(
            id=updated_product["id"],
            name=updated_product["name"],
            description=updated_product["description"],
            price=updated_product["price"],
            category=updated_product["category"],
            images=updated_product["images"],
            is_available=updated_product["is_available"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update product: {str(e)}"
        )


@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_product(
    product_id: int,
    current_user: UserResponse = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Delete a product - soft delete (sets is_available to False). Admin only."""
    try:
        deleted_product = db.delete_product(product_id)
        
        return ProductResponse(
            id=deleted_product["id"],
            name=deleted_product["name"],
            description=deleted_product["description"],
            price=deleted_product["price"],
            category=deleted_product["category"],
            images=deleted_product["images"],
            is_available=deleted_product["is_available"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

