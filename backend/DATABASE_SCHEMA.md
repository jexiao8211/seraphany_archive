# Database Schema Documentation

This document describes the database schema for the Vintage Store project.

## Overview

Our database uses PostgreSQL with Prisma ORM and includes the following models:

- **User**: Customer accounts and authentication
- **Product**: Vintage items for sale
- **Order**: Customer purchases
- **OrderItem**: Individual items within orders

## Models

### User Model
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  firstName String
  lastName  String
  password  String   // Hashed password
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relationships
  orders Order[]

  @@map("users")
}
```

**Purpose**: Stores customer account information
**Key Fields**:
- `email`: Unique identifier for login
- `password`: Hashed password for security
- `firstName/lastName`: Customer name
- `orders`: One-to-many relationship with orders

### Product Model
```prisma
model Product {
  id          Int      @id @default(autoincrement())
  name        String
  description String
  price       Decimal  @db.Decimal(10, 2)
  category    String
  images      String[] // Array of image URLs
  isAvailable Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // Relationships
  orderItems OrderItem[]

  @@map("products")
}
```

**Purpose**: Stores vintage items for sale
**Key Fields**:
- `name`: Product name
- `price`: Price in decimal format (10 digits total, 2 decimal places)
- `category`: Product category (dresses, bags, shoes, accessories)
- `images`: Array of image URLs
- `isAvailable`: Soft delete flag
- `orderItems`: One-to-many relationship with order items

### Order Model
```prisma
model Order {
  id            Int      @id @default(autoincrement())
  userId        Int
  totalAmount   Decimal  @db.Decimal(10, 2)
  status        OrderStatus @default(PENDING)
  shippingAddress Json? // Store as JSON for flexibility
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  // Relationships
  user  User        @relation(fields: [userId], references: [id], onDelete: Cascade)
  items OrderItem[]

  @@map("orders")
}
```

**Purpose**: Stores customer orders
**Key Fields**:
- `userId`: Foreign key to User
- `totalAmount`: Total order amount
- `status`: Order status (PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED)
- `shippingAddress`: JSON field for flexible address storage
- `user`: Many-to-one relationship with User
- `items`: One-to-many relationship with OrderItem

### OrderItem Model
```prisma
model OrderItem {
  id        Int     @id @default(autoincrement())
  orderId   Int
  productId Int
  quantity  Int
  price     Decimal @db.Decimal(10, 2) // Price at time of purchase

  // Relationships
  order   Order   @relation(fields: [orderId], references: [id], onDelete: Cascade)
  product Product @relation(fields: [productId], references: [id])

  @@map("order_items")
}
```

**Purpose**: Stores individual items within orders
**Key Fields**:
- `orderId`: Foreign key to Order
- `productId`: Foreign key to Product
- `quantity`: Number of items
- `price`: Price at time of purchase (for historical accuracy)
- `order`: Many-to-one relationship with Order
- `product`: Many-to-one relationship with Product

### OrderStatus Enum
```prisma
enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}
```

**Purpose**: Defines possible order statuses
**Values**:
- `PENDING`: Order created but not confirmed
- `CONFIRMED`: Order confirmed by customer
- `SHIPPED`: Order shipped to customer
- `DELIVERED`: Order delivered to customer
- `CANCELLED`: Order cancelled

## Relationships

### User → Order (One-to-Many)
- One user can have many orders
- Each order belongs to one user
- Cascade delete: If user is deleted, their orders are deleted

### Order → OrderItem (One-to-Many)
- One order can have many order items
- Each order item belongs to one order
- Cascade delete: If order is deleted, its items are deleted

### Product → OrderItem (One-to-Many)
- One product can be in many order items
- Each order item references one product
- No cascade delete: Products are preserved for historical data

## Data Types

### Decimal Fields
- `price`: `@db.Decimal(10, 2)` - 10 digits total, 2 decimal places
- `totalAmount`: `@db.Decimal(10, 2)` - Same format for consistency

### JSON Fields
- `shippingAddress`: Flexible storage for address information
- Allows for different address formats without schema changes

### Array Fields
- `images`: `String[]` - Array of image URLs
- Allows multiple product images

## Indexes and Constraints

### Unique Constraints
- `User.email`: Unique email addresses
- `User.id`: Primary key
- `Product.id`: Primary key
- `Order.id`: Primary key
- `OrderItem.id`: Primary key

### Foreign Key Constraints
- `Order.userId` → `User.id`
- `OrderItem.orderId` → `Order.id`
- `OrderItem.productId` → `Product.id`

### Cascade Deletes
- `Order` → `User`: Cascade delete
- `OrderItem` → `Order`: Cascade delete
- `OrderItem` → `Product`: No cascade (preserve products)

## Sample Data

### Sample Products
```json
{
  "name": "Vintage Chanel Dress",
  "description": "Beautiful vintage Chanel dress from the 1980s",
  "price": 1500.00,
  "category": "dresses",
  "images": ["https://example.com/chanel-dress-1.jpg"],
  "isAvailable": true
}
```

### Sample User
```json
{
  "email": "customer@example.com",
  "firstName": "Jane",
  "lastName": "Doe",
  "password": "hashed_password_here"
}
```

### Sample Order
```json
{
  "userId": 1,
  "totalAmount": 1500.00,
  "status": "PENDING",
  "shippingAddress": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001",
    "country": "USA"
  }
}
```

## Performance Considerations

### Indexing
- Primary keys are automatically indexed
- Foreign keys should be indexed for join performance
- Consider adding indexes on frequently queried fields

### Query Optimization
- Use `include` to fetch related data in one query
- Use `select` to fetch only needed fields
- Use pagination for large result sets

### Data Volume
- **Products**: ~100 active items (small dataset)
- **Orders**: ~1000 historical orders (growing but manageable)
- **Users**: Global customers (potentially large)

## Security Considerations

### Password Storage
- Passwords are hashed before storage
- Use bcrypt or similar for password hashing
- Never store plain text passwords

### Data Validation
- Validate all input data
- Use Prisma's built-in validation
- Sanitize user inputs

### Access Control
- Implement proper authentication
- Use JWT tokens for API access
- Validate user permissions for operations

## Migration Strategy

### Schema Changes
1. Update `prisma/schema.prisma`
2. Run `poetry run prisma db push`
3. Update application code
4. Test thoroughly

### Data Migration
1. Backup existing data
2. Run migration scripts
3. Verify data integrity
4. Update application code

## Monitoring and Maintenance

### Database Health
- Monitor connection pool usage
- Track query performance
- Set up alerts for errors

### Backup Strategy
- Regular automated backups
- Test restore procedures
- Store backups securely

### Scaling Considerations
- Connection pooling for high traffic
- Read replicas for read-heavy workloads
- Database sharding for very large datasets
