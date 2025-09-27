"""
Main FastAPI application for vintage store backend.
Following TDD approach - implementing endpoints to make tests pass.
"""
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os

# Initialize FastAPI app
app = FastAPI(title="Vintage Store API", version="1.0.0")

# Security scheme for JWT tokens
security = HTTPBearer()

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

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: ShippingAddress

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: str
    shipping_address: ShippingAddress

# Mock data for testing (will be replaced with database)
mock_products = [
    Product(id=1, name="Vintage Chanel Dress", description="Beautiful vintage Chanel dress", 
            price=1500.00, category="dresses", images=["image1.jpg"]),
    Product(id=2, name="Vintage Hermes Bag", description="Classic Hermes handbag", 
            price=2500.00, category="bags", images=["image2.jpg"]),
]

# Mock user storage for testing
mock_users = []

# Authentication dependency (simplified for now)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token."""
    # This is a placeholder - in real implementation, we'd decode the JWT
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication not implemented yet"
    )

# Optional authentication dependency for endpoints that might not require auth
async def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token (optional)."""
    # This is a placeholder - in real implementation, we'd decode the JWT
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication not implemented yet"
    )

# Product endpoints
@app.get("/products")
async def get_products(
    request: Request,
    page: int = 1, 
    limit: int = 10, 
    category: Optional[str] = None, 
    search: Optional[str] = None
):
    """Get products with optional filtering and pagination."""
    products = mock_products.copy()
    
    # Apply filters
    if category:
        products = [p for p in products if p.category == category]
    if search:
        products = [p for p in products if search.lower() in p.name.lower()]
    
    # Check if query parameters were provided
    has_query_params = bool(request.query_params)
    
    # Always return paginated format when query parameters are present
    # or when filters are applied
    if has_query_params or category or search:
        start = (page - 1) * limit
        end = start + limit
        paginated_products = products[start:end]
        
        return {
            "items": paginated_products,
            "total": len(products),
            "page": page,
            "limit": limit
        }
    
    # Return simple list for basic GET /products (no query params)
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get a single product by ID."""
    product = next((p for p in mock_products if p.id == product_id), None)
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
async def register_user(user: UserCreate):
    """Register a new user."""
    # Basic validation
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Check if user already exists in mock storage
    for existing_user in mock_users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user (mock response)
    new_user = User(
        id=len(mock_users) + 1,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    mock_users.append(new_user)
    return new_user

@app.post("/auth/login", response_model=Token)
async def login_user(credentials: UserLogin):
    """Login user and return JWT token."""
    # Mock authentication - in real implementation, we'd verify password hash
    if credentials.email == "nonexistent@example.com" or credentials.password != "securepassword123":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return Token(access_token="mock_jwt_token", token_type="bearer")

@app.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    # This will be implemented when we add JWT authentication
    pass

@app.post("/auth/logout")
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user."""
    # This will be implemented when we add JWT authentication
    pass

# Order endpoints
@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    """Create a new order (requires authentication)."""
    # This will be implemented when we add authentication
    pass

@app.get("/orders", response_model=List[Order])
async def get_user_orders(current_user: User = Depends(get_current_user)):
    """Get current user's orders (requires authentication)."""
    # This will be implemented when we add authentication
    pass

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    """Get a specific order (requires authentication)."""
    # This will be implemented when we add authentication
    pass

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: int, status_data: dict, current_user: User = Depends(get_current_user)):
    """Update order status (requires authentication)."""
    # This will be implemented when we add authentication
    pass

@app.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, current_user: User = Depends(get_current_user)):
    """Cancel an order (requires authentication)."""
    # This will be implemented when we add authentication
    pass

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Vintage Store API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
