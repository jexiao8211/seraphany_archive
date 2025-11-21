"""
Main FastAPI application for vintage store backend.
Following TDD approach - implementing endpoints to make tests pass.
"""
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import os
from .database import DatabaseService
from .auth import AuthService
from .storage import storage_service
from .config import settings

# Initialize FastAPI app
app = FastAPI(title=settings.app_name, version=settings.app_version)

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

# Security scheme for JWT tokens
security = HTTPBearer(auto_error=False)

# Dependency injection for database service
def get_database_service() -> DatabaseService:
    """Get database service instance"""
    return DatabaseService()

# Pydantic models for request/response
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    images: List[str] = []

class Product(ProductBase):
    id: int
    is_available: bool = True

class ProductCreate(ProductBase):
    pass

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRefresh(BaseModel):
    refresh_token: str

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: ShippingAddress

class Order(BaseModel):
    id: int
    user_id: int
    items: List[Dict[str, Any]]  # Simple list of item dictionaries
    total_amount: float
    status: str
    shipping_address: ShippingAddress
    created_at: str
    updated_at: str

class OrderStatusUpdate(BaseModel):
    status: str

class AdminStatusUpdate(BaseModel):
    is_admin: bool

# Mock data for testing (will be replaced with database)
mock_products = [
    Product(id=1, name="Vintage Chanel Dress", description="Beautiful vintage Chanel dress", 
            price=1500.00, category="dresses", images=["image1.jpg"]),
    Product(id=2, name="Vintage Hermes Bag", description="Classic Hermes handbag", 
            price=2500.00, category="bags", images=["image2.jpg"]),
]

# Mock user storage for testing
mock_users = []

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: DatabaseService = Depends(get_database_service)
):
    """Get current user from JWT token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Extract user ID from token
        user_id = AuthService.get_user_id_from_token(credentials.credentials)
        
        # Get user from database
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return User(
            id=user["id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_admin=user.get("is_admin", False)
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Optional authentication dependency for endpoints that might not require auth
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: DatabaseService = Depends(get_database_service)
):
    """Get current user from JWT token (optional)."""
    if not credentials:
        return None
    
    try:
        # Extract user ID from token
        user_id = AuthService.get_user_id_from_token(credentials.credentials)
        
        # Get user from database
        user = db.get_user(user_id)
        if not user:
            return None
        
        return User(
            id=user["id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_admin=user.get("is_admin", False)
        )
    except Exception:
        return None

# Admin authentication dependency
async def get_admin_user(current_user: User = Depends(get_current_user)):
    """Get current admin user (requires authentication and admin role)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Product endpoints
@app.get("/products")
async def get_products(
    page: int = 1, 
    limit: int = 100,  # Increased default for better UX
    category: Optional[str] = None, 
    search: Optional[str] = None,
    db: DatabaseService = Depends(get_database_service)
):
    """Get products with optional filtering and pagination."""
    # Always return consistent format with pagination metadata
    result = db.get_products(page=page, limit=limit, category=category, search=search)
    return result

@app.get("/products/{product_id}")
async def get_product(product_id: int, db: DatabaseService = Depends(get_database_service)):
    """Get a single product by ID."""
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, 
    current_user: User = Depends(get_admin_user), 
    db: DatabaseService = Depends(get_database_service)
):
    """Create a new product (requires authentication)."""
    try:
        # Convert Pydantic model to dict for database
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "images": product.images,
            "is_available": True  # New products are available by default
        }
        
        # Create product in database
        created_product = db.create_product(product_data)
        
        # Return the created product
        return Product(
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

@app.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int, 
    product: ProductCreate, 
    current_user: User = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Update a product (requires authentication)."""
    try:
        # Convert Pydantic model to dict for database
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "images": product.images
        }
        
        # Update product in database
        updated_product = db.update_product(product_id, product_data)
        
        # Return the updated product
        return Product(
            id=updated_product["id"],
            name=updated_product["name"],
            description=updated_product["description"],
            price=updated_product["price"],
            category=updated_product["category"],
            images=updated_product["images"],
            is_available=updated_product["is_available"]
        )
        
    except ValueError as e:
        # Database raises ValueError when product not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update product: {str(e)}"
        )

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(
    product_id: int, 
    current_user: User = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """
    Delete a product (soft delete - sets is_available to False).
    Requires authentication.
    """
    try:
        # Soft delete the product (sets is_available = False)
        deleted_product = db.delete_product(product_id)
        
        # Return the deleted product with is_available = False
        return Product(
            id=deleted_product["id"],
            name=deleted_product["name"],
            description=deleted_product["description"],
            price=deleted_product["price"],
            category=deleted_product["category"],
            images=deleted_product["images"],
            is_available=deleted_product["is_available"]
        )
        
    except ValueError as e:
        # Database raises ValueError when product not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

# Image upload endpoints
@app.post("/upload/product-images", status_code=status.HTTP_201_CREATED)
async def upload_product_images(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_admin_user)
):
    """
    Upload product images (admin-only).
    Accepts multiple image files with validation.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
    
    uploaded_paths = []
    errors = []
    
    for file in files:
        try:
            # Read file content
            content = await file.read()
            
            # Validate file
            is_valid, error_msg = storage_service.validate_image_file(
                file.filename, 
                len(content)
            )
            
            if not is_valid:
                errors.append(f"{file.filename}: {error_msg}")
                continue
            
            # Save file
            url_path = storage_service.save_image(content, file.filename, "products")
            uploaded_paths.append(url_path)
            
        except Exception as e:
            errors.append(f"{file.filename}: Upload failed - {str(e)}")
    
    if errors and not uploaded_paths:
        # All uploads failed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"All uploads failed: {'; '.join(errors)}"
        )
    
    return {
        "uploaded_paths": uploaded_paths,
        "errors": errors,
        "message": f"Successfully uploaded {len(uploaded_paths)} file(s)"
    }

# Authentication endpoints
@app.post("/auth/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: DatabaseService = Depends(get_database_service)):
    """Register a new user."""
    
    # Basic validation
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Check if user already exists
    existing_user = db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password  # In production, hash this password
    }
    
    new_user = db.create_user(user_data)
    return User(
        id=new_user["id"],
        email=new_user["email"],
        first_name=new_user["first_name"],
        last_name=new_user["last_name"],
        is_admin=new_user.get("is_admin", False)
    )

@app.post("/auth/login", response_model=Token)
async def login_user(credentials: UserLogin, db: DatabaseService = Depends(get_database_service)):
    """Login user and return JWT token."""
    
    # Verify user credentials
    user = db.verify_user_credentials(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token = AuthService.create_access_token(data={"sub": str(user["id"])})
    return Token(access_token=access_token, token_type="bearer")

@app.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@app.post("/auth/logout")
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user."""
    # For JWT tokens, logout is handled client-side by removing the token
    # In a more sophisticated setup, you might maintain a blacklist of tokens
    return {"message": "Successfully logged out"}

@app.post("/auth/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh):
    """Refresh JWT token."""
    try:
        # Verify the current token
        payload = AuthService.verify_token(token_data.refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Create new token
        access_token = AuthService.create_access_token(data={"sub": user_id})
        return Token(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Order endpoints
@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: DatabaseService = Depends(get_database_service)):
    """Create a new order (requires authentication)."""
    try:
        # Validate products exist and are available
        total_amount = 0.0
        order_items = []
        
        for item in order.items:
            # Get product details
            product = db.get_product(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with ID {item.product_id} not found"
                )
            
            if not product.get("is_available", True):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product['name']} is not available"
                )
            
            if item.quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quantity must be greater than 0"
                )
            
            # Calculate item total
            item_total = float(product["price"]) * item.quantity
            total_amount += item_total
            
            order_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(product["price"]),
                "product_name": product["name"]
            })
        
        # Create order data
        order_data = {
            "user_id": current_user.id,
            "total_amount": total_amount,
            "status": "PENDING",
            "shipping_address": order.shipping_address.model_dump(),
            "items": order_items
        }
        
        # Create order in database
        created_order = db.create_order(order_data)
        
        return Order(
            id=created_order["id"],
            user_id=created_order["user_id"],
            items=created_order["items"],  # Direct list of item dictionaries
            total_amount=created_order["total_amount"],
            status=created_order["status"],
            shipping_address=ShippingAddress(**created_order["shipping_address"]),
            created_at=created_order["created_at"],
            updated_at=created_order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )

@app.get("/orders", response_model=List[Order])
async def get_user_orders(current_user: User = Depends(get_current_user), db: DatabaseService = Depends(get_database_service)):
    """Get current user's orders (requires authentication)."""
    try:
        orders = db.get_user_orders(current_user.id)
        
        return [
            Order(
                id=order["id"],
                user_id=order["user_id"],
                items=order["items"],  # Direct list of item dictionaries
                total_amount=order["total_amount"],
                status=order["status"],
                shipping_address=ShippingAddress(**order["shipping_address"]),
                created_at=order["created_at"],
                updated_at=order["updated_at"]
            ) for order in orders
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orders: {str(e)}"
        )

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int, current_user: User = Depends(get_current_user), db: DatabaseService = Depends(get_database_service)):
    """Get a specific order (requires authentication)."""
    try:
        order = db.get_order(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Check if the order belongs to the current user
        if order["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only view your own orders."
            )
        
        return Order(
            id=order["id"],
            user_id=order["user_id"],
            items=order["items"],  # Direct list of item dictionaries
            total_amount=order["total_amount"],
            status=order["status"],
            shipping_address=ShippingAddress(**order["shipping_address"]),
            created_at=order["created_at"],
            updated_at=order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get order: {str(e)}"
        )

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: int, status_data: OrderStatusUpdate, current_user: User = Depends(get_current_user), db: DatabaseService = Depends(get_database_service)):
    """Update order status (requires authentication)."""
    try:
        # First check if the order exists and belongs to the user
        order = db.get_order(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        if order["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only update your own orders."
            )
        
        # Validate status
        valid_statuses = ["PENDING", "CONFIRMED", "SHIPPED", "DELIVERED", "CANCELLED"]
        if status_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Update the order status
        updated_order = db.update_order_status(order_id, status_data.status)
        
        return {
            "message": "Order status updated successfully",
            "order_id": updated_order["id"],
            "new_status": updated_order["status"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update order status: {str(e)}"
        )

@app.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, current_user: User = Depends(get_current_user), db: DatabaseService = Depends(get_database_service)):
    """Cancel an order (requires authentication)."""
    try:
        # First check if the order exists and belongs to the user
        order = db.get_order(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        if order["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only cancel your own orders."
            )
        
        # Check if order can be cancelled (not already delivered or cancelled)
        if order["status"] in ["DELIVERED", "CANCELLED"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel order with status: {order['status']}"
            )
        
        # Cancel the order
        updated_order = db.update_order_status(order_id, "CANCELLED")
        
        return {
            "message": "Order cancelled successfully",
            "order_id": updated_order["id"],
            "status": updated_order["status"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel order: {str(e)}"
        )

# Admin user management endpoints
@app.get("/admin/users", response_model=Dict[str, Any])
async def get_all_users(
    page: int = 1,
    limit: int = 100,
    current_user: User = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Get all users (admin only)."""
    try:
        users = db.get_all_users(page=page, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )

@app.put("/admin/users/{user_id}/admin-status", response_model=User)
async def update_user_admin_status(
    user_id: int,
    admin_status: AdminStatusUpdate,
    current_user: User = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Update a user's admin status (admin only)."""
    try:
        # Prevent users from removing their own admin status
        if user_id == current_user.id and not admin_status.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot remove your own admin status"
            )
        
        updated_user = db.update_user_admin_status(user_id, admin_status.is_admin)
        return User(
            id=updated_user["id"],
            email=updated_user["email"],
            first_name=updated_user["first_name"],
            last_name=updated_user["last_name"],
            is_admin=updated_user["is_admin"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user admin status: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Vintage Store API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
