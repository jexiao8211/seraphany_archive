# Vintage Designer Ecommerce Website - Project Requirements

## Project Overview
A simple ecommerce website for a vintage designer store, targeting global customers with a clean, Shopify-like interface.

## Business Requirements

### Scale & Scope
- **Current inventory**: Never more than 100 items for sale at any time
- **Historical data**: Track all sold items (growing dataset, max ~1000 total)
- **Target market**: Global customers
- **Design**: Clean, Shopify-like appearance

### Core Features Required
- Product catalog with categories
- Shopping cart and checkout
- User accounts and order history
- Payment processing
- Inventory management
- Image galleries for products
- Search and filtering

### Features to Skip (For Now)
- Admin dashboard for managing products
- Email notifications for orders
- Shipping calculations
- Tax calculations

## Technical Requirements

### Frontend Stack
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Clean, modern UI (Shopify-like)
- **Deployment**: Cost-effective hosting

### Backend Stack
- **Framework**: FastAPI
- **Package Manager**: poetry 
- **Database**: PostgreSQL (for scalability and data integrity)
- **ORM**: Prisma or SQLAlchemy
- **Authentication**: JWT-based or session-based
- **Payments**: Stripe integration

### Cost Optimization
- Use free/low-cost hosting options
- Optimize for minimal infrastructure costs
- Efficient database queries for small dataset

## Data Model Considerations

### Products
- Basic product information (name, description, price, images)
- Categories and tags for filtering
- Inventory status (available/sold)
- Historical tracking of sold items

### Users
- Basic profile information
- Order history
- Authentication credentials

### Orders
- Order details and status
- Customer information
- Payment information
- Timestamps for tracking

## Development Approach

### Phase 1: Core Functionality
1. Set up project structure (React + Vite frontend, FastAPI backend)
2. Implement basic product catalog
3. Add shopping cart functionality
4. Integrate Stripe payments
5. Basic user authentication

### Phase 2: Enhanced Features
1. Product search and filtering
2. User order history
3. Image optimization
4. Responsive design improvements

### Phase 3: Admin Features (Future)
1. Product management interface
2. Order management
3. Analytics dashboard

## Key Design Principles
- **SOLID principles**: Maintainable, extensible code
- **DRY**: Avoid code duplication
- **Performance**: Fast loading for global users
- **Simplicity**: Clean, intuitive user experience
- **Cost-effective**: Minimal hosting and operational costs

## Success Criteria
- Fast, responsive website that works globally
- Easy product management for store owner
- Secure payment processing
- Clean, professional appearance similar to Shopify
- Low operational costs
- Scalable architecture for future growth

## Notes
- User is a beginner SWE, so code should be well-commented and follow best practices
- Focus on learning and understanding the codebase
- Be honest about technical decisions and trade-offs
- Prioritize simplicity and maintainability over complex features
