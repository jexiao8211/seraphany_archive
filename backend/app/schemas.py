"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime


# ============== User Schemas ==============

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response (excludes password)"""
    id: int
    is_admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


# ============== Product Schemas ==============

class ProductBase(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    images: List[str] = Field(default_factory=list)


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    images: Optional[List[str]] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    is_available: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Schema for paginated product list"""
    items: List[ProductResponse]
    total: int
    page: int
    limit: int


# ============== Order Schemas ==============

class ShippingAddress(BaseModel):
    """Schema for shipping address"""
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    zip_code: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)


class OrderItemCreate(BaseModel):
    """Schema for creating an order item"""
    product_id: int
    quantity: int = Field(..., gt=0)

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v


class OrderCreate(BaseModel):
    """Schema for creating an order"""
    items: List[OrderItemCreate] = Field(..., min_length=1)
    shipping_address: ShippingAddress


class OrderItemResponse(BaseModel):
    """Schema for order item response"""
    id: Optional[int] = None
    product_id: int
    quantity: int
    price: float
    product_name: str


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: Optional[ShippingAddress] = None
    items: List[OrderItemResponse] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status"""
    status: str = Field(..., pattern="^(PENDING|CONFIRMED|SHIPPED|DELIVERED|CANCELLED)$")


class OrderStatusResponse(BaseModel):
    """Schema for order status update response"""
    message: str
    order_id: int
    new_status: str


class OrderCancelResponse(BaseModel):
    """Schema for order cancellation response"""
    message: str
    order_id: int
    status: str


# ============== Upload Schemas ==============

class ImageUploadResponse(BaseModel):
    """Schema for image upload response"""
    uploaded_paths: List[str]
    errors: List[str] = Field(default_factory=list)
    message: str


# ============== Common Schemas ==============

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str


# ============== Admin Schemas ==============

class AdminStatusUpdate(BaseModel):
    """Schema for updating user admin status"""
    is_admin: bool


class UserListResponse(BaseModel):
    """Schema for paginated user list"""
    items: List[UserResponse]
    total: int
    page: int
    limit: int

