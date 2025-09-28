# Database Schema Documentation

This document describes the database schema for the Vintage Store project.

## Overview

Our database uses PostgreSQL with SQLAlchemy ORM and includes the following models:

- **User**: Customer accounts and authentication
- **Product**: Vintage items for sale
- **Order**: Customer purchases
- **OrderItem**: Individual items within orders

## Architecture

### Database Service Pattern
We use a **Database Service** pattern with **Dependency Injection** for clean separation between production and testing:

```python
# Production: Real PostgreSQL database
def get_database_service() -> DatabaseService:
    return DatabaseService()  # Uses PostgreSQL via DATABASE_URL

# Testing: In-memory SQLite database
app.dependency_overrides[get_database_service] = lambda: test_db_service
```

### Key Benefits:
- **Testability**: Easy to inject test database
- **Flexibility**: Can switch databases without code changes
- **Maintainability**: Clear separation of concerns
- **Performance**: Fast tests with in-memory SQLite

## Models

### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
```

**Purpose**: Stores customer account information
**Key Fields**:
- `email`: Unique identifier for login
- `password`: Hashed password for security
- `first_name/last_name`: Customer name (snake_case convention)
- `orders`: One-to-many relationship with orders

### Product Model
```python
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # 10 digits total, 2 decimal places
    category = Column(String, nullable=False)
    images = Column(Text)  # JSON string of image URLs
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")
```

**Purpose**: Stores vintage items for sale
**Key Fields**:
- `name`: Product title
- `description`: Detailed product information
- `price`: Decimal with 2 decimal places for currency
- `category`: Product category (dresses, bags, etc.)
- `images`: JSON array of image URLs
- `is_available`: Soft delete flag (snake_case convention)
- `order_items`: One-to-many relationship with order items

**Helper Methods**:
```python
def get_images(self) -> List[str]:
    """Get images as a list"""
    if self.images:
        return json.loads(self.images)
    return []

def set_images(self, images_list: List[str]):
    """Set images from a list"""
    self.images = json.dumps(images_list)
```

### Order Model
```python
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="PENDING", nullable=False)
    shipping_address = Column(Text)  # JSON string for flexibility
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
```

**Purpose**: Represents customer purchases
**Key Fields**:
- `user_id`: Foreign key to User
- `total_amount`: Total order value
- `status`: Order status (PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED)
- `shipping_address`: JSON object with address details
- `items`: One-to-many relationship with order items

**Helper Methods**:
```python
def get_shipping_address(self) -> Dict[str, Any]:
    """Get shipping address as a dict"""
    if self.shipping_address:
        return json.loads(self.shipping_address)
    return None

def set_shipping_address(self, address_dict: Dict[str, Any]):
    """Set shipping address from a dict"""
    self.shipping_address = json.dumps(address_dict)
```

### OrderItem Model
```python
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
```

**Purpose**: Individual items within an order
**Key Fields**:
- `order_id`: Foreign key to Order
- `product_id`: Foreign key to Product
- `quantity`: Number of items ordered
- `price`: Price at time of purchase (for historical accuracy)

## Database Service Layer

### DatabaseService Class
```python
class DatabaseService:
    """Database service class for handling all database operations"""
    
    def get_session(self) -> Session:
        """Get database session with context manager"""
        return SessionLocal()
    
    # All methods use: with self.get_session() as session:
    def get_products(self, page=1, limit=10, category=None, search=None):
        # Implementation with proper session management
```

**Key Features**:
- **Context Managers**: Automatic session cleanup
- **Transaction Safety**: Automatic commit/rollback
- **Connection Pooling**: Efficient database connections
- **Error Handling**: Proper exception management

### Dependency Injection
```python
# In main.py
def get_database_service() -> DatabaseService:
    """Dependency injection for database service"""
    return DatabaseService()

# In endpoints
@app.get("/products")
async def get_products(db: DatabaseService = Depends(get_database_service)):
    return db.get_products()
```

## Testing Architecture

### Test Database Configuration
```python
# In conftest.py
@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db_service(test_db):
    """Create a test database service with the test session"""
    class TestDatabaseService(DatabaseService):
        def get_session(self):
            return test_db
    return TestDatabaseService()

@pytest.fixture(scope="function")
def client(test_db, test_db_service):
    """Create a test client with overridden database dependency"""
    app.dependency_overrides[get_database_service] = lambda: test_db_service
    yield TestClient(app)
    app.dependency_overrides.clear()
```

**Benefits**:
- **Isolation**: Each test gets fresh database
- **Speed**: In-memory SQLite is much faster
- **Reliability**: No external dependencies
- **Parallel**: Tests can run concurrently

## Migration from Prisma

### Key Changes Made:
1. **ORM Migration**: Prisma → SQLAlchemy
2. **Naming Convention**: camelCase → snake_case
3. **Database Reset**: Clean slate with new schema
4. **Dependency Injection**: Proper test/prod separation

### Column Name Changes:
- `firstName` → `first_name`
- `lastName` → `last_name`
- `isAvailable` → `is_available`
- `createdAt` → `created_at`
- `updatedAt` → `updated_at`

## Database Configuration

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost/vintage_store
```

### Database Setup
```python
# In database_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
```

## Best Practices

### 1. Session Management
- Always use context managers: `with self.get_session() as session:`
- Automatic commit/rollback on success/failure
- Proper connection cleanup

### 2. Error Handling
- Graceful handling of database errors
- Proper HTTP status codes
- User-friendly error messages

### 3. Performance
- Connection pooling for production
- Efficient queries with proper indexing
- Pagination for large datasets

### 4. Testing
- Use dependency injection for testability
- In-memory database for fast tests
- Proper test isolation
- Mock external dependencies

## API Response Format

### Products
```json
{
  "items": [
    {
      "id": 1,
      "name": "Vintage Chanel Dress",
      "description": "Beautiful vintage dress",
      "price": 1500.00,
      "category": "dresses",
      "images": ["image1.jpg", "image2.jpg"],
      "isAvailable": true,
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

### Users
```json
{
  "id": 1,
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

### Orders
```json
{
  "id": 1,
  "userId": 1,
  "totalAmount": 1500.00,
  "status": "PENDING",
  "shippingAddress": {
    "street": "123 Main St",
    "city": "New York",
    "zipCode": "10001"
  },
  "items": [
    {
      "id": 1,
      "productId": 1,
      "quantity": 1,
      "price": 1500.00,
      "product": {
        "id": 1,
        "name": "Vintage Chanel Dress",
        "description": "Beautiful vintage dress",
        "price": 1500.00,
        "category": "dresses",
        "images": ["image1.jpg"]
      }
    }
  ],
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

This schema provides a solid foundation for the Vintage Store application with proper separation of concerns, testability, and maintainability.