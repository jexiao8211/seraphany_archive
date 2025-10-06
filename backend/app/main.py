"""
Main FastAPI application for vintage store backend.
Following TDD approach - implementing endpoints to make tests pass.
"""
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import os
from .database import DatabaseService
from .auth import AuthService

# Initialize FastAPI app
app = FastAPI(title="Vintage Store API", version="1.0.0")

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            last_name=user["last_name"]
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
            last_name=user["last_name"]
        )
    except Exception:
        return None

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

@app.post("/products")
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user)):
    """Create a new product (requires authentication)."""
    # This will be implemented when we add authentication
    pass

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductCreate, current_user: User = Depends(get_current_user)):
    """Update a product (requires authentication)."""
    # This will be implemented when we add authentication
    pass

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, current_user: User = Depends(get_current_user)):
    """Delete a product (requires authentication)."""
    # This will be implemented when we add authentication
    pass

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
        last_name=new_user["last_name"]
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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Vintage Store API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
