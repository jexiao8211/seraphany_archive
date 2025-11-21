# Database Management Guide

This guide explains how to add and manage data in your database, including creating admin users.

## Table of Contents
1. [Creating an Admin User](#creating-an-admin-user)
2. [Adding Products](#adding-products)
3. [Other Ways to Add Data](#other-ways-to-add-data)
4. [Production vs Development](#production-vs-development)

---

## Creating an Admin User

### Method 1: Using the Script (Recommended)

We've created a script `create_admin.py` that makes it easy to create an admin user.

#### From the backend directory:

```bash
# Interactive mode (will prompt for details)
poetry run python create_admin.py

# Or with environment variables
ADMIN_EMAIL=admin@example.com \
ADMIN_PASSWORD=securepassword123 \
ADMIN_FIRST_NAME=Admin \
ADMIN_LAST_NAME=User \
poetry run python create_admin.py
```

#### What it does:
- Creates a new user with `is_admin=True`
- Hashes the password automatically
- Checks if user already exists and offers to promote them to admin
- Validates password length (minimum 8 characters)

#### Example output:
```
==================================================
Create Admin User
==================================================
Enter admin email: admin@example.com
Enter admin password (min 8 characters): ********
Confirm password: ********
Enter first name (default: Admin): 
Enter last name (default: User): 

Creating admin user...
[SUCCESS] Admin user created successfully!
  Email: admin@example.com
  Name: Admin User
  User ID: 1
  Admin: True
```

### Method 2: Direct Database Access (Advanced)

If you have direct database access (e.g., via Railway's database dashboard or psql):

```sql
-- First, you need to hash the password using the same method
-- This is more complex and not recommended unless you understand password hashing
-- The password hash format depends on your AuthService configuration
```

**Note:** This method is not recommended because:
- You need to manually hash passwords using the same algorithm
- It's error-prone and less secure
- The script method is much easier and safer

### Method 3: Using Python Interactively

You can also use Python directly:

```python
from app.database import DatabaseService

db = DatabaseService()
user_data = {
    "email": "admin@example.com",
    "password": "yourpassword123",  # Will be hashed automatically
    "first_name": "Admin",
    "last_name": "User",
    "is_admin": True
}
user = db.create_user(user_data)
print(f"Created admin user: {user['email']}")
```

---

## Adding Products

### Method 1: Using the Seed Script

We have a `seed_products.py` script for adding sample products:

```bash
# From the backend directory
poetry run python seed_products.py
```

This adds 6 sample products to your database.

### Method 2: Using the Admin API

Once you have an admin user, you can use the API to add products:

```bash
# First, login to get a token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "yourpassword"
  }'

# Use the token to create a product
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vintage Dress",
    "description": "Beautiful vintage dress",
    "price": 99.99,
    "category": "dresses",
    "images": ["/uploads/products/dress1.jpg"]
  }'
```

### Method 3: Using Python Script

Create your own script similar to `seed_products.py`:

```python
from app.database import DatabaseService

db = DatabaseService()

product_data = {
    "name": "Your Product Name",
    "description": "Product description",
    "price": 99.99,
    "category": "dresses",  # or "bags", "shoes", "accessories"
    "images": ["/uploads/products/image.jpg"],
    "is_available": True
}

product = db.create_product(product_data)
print(f"Created product: {product['name']}")
```

---

## Other Ways to Add Data

### 1. **Via API Endpoints** (Recommended for Production)
- Use the REST API endpoints defined in `app/main.py`
- Requires authentication for admin operations
- Best for production environments
- Example: Frontend admin panel, API clients

### 2. **Via Seed Scripts** (Recommended for Development)
- Use scripts like `seed_products.py` and `create_admin.py`
- Good for initial setup and development
- Can be run manually or in CI/CD pipelines

### 3. **Direct Database Access** (Advanced)
- Use SQL directly via database client
- **Warning:** Bypasses application logic (password hashing, validation, etc.)
- Only recommended for advanced users who understand the database schema
- Not recommended for creating users (password hashing is complex)

### 4. **Via Database Migrations**
- Use Alembic migrations for schema changes
- Not for adding data, but for modifying database structure
- See `ALEMBIC_GUIDE.md` for more info

---

## Production vs Development

### Development (Local)
- Use seed scripts freely
- Can directly access database
- Can use Python scripts interactively
- Easier to experiment and test

### Production (Railway/Cloud)
- **Create First Admin User:** Use Railway's CLI, script, or connect to database (bootstrap problem)
- **Manage Admin Users:** Use the admin API endpoints (`/admin/users/*`) - **Recommended**
- **Add Products:** Use the admin API endpoints (via frontend or API client)
- **Best Practice:** 
  - Use API endpoints for ongoing data management
  - Direct database access should only be used for initial setup (first admin)
  - Use migrations for schema changes
  - Never directly modify production database for routine operations

### Creating Admin User in Production (Railway)

#### Option 1: Railway CLI with `railway run` (Recommended)

This is the **easiest and recommended method**. The `railway run` command runs your script locally but with your production environment variables (including `DATABASE_URL`).

**Prerequisites:**
1. Install Railway CLI (if not already installed):
   ```bash
   # Windows (PowerShell)
   scoop install railway
   
   # macOS
   brew install railway
   
   # Or via npm (all platforms)
   npm i -g @railway/cli
   ```

2. Authenticate with Railway:
   ```bash
   railway login
   ```

3. Link to your project (from your backend directory):
   ```bash
   cd backend
   railway link
   ```
   This will prompt you to select your team, project, and **environment** (make sure to select **production**).

**Run the script:**

**Method A: Interactive (will prompt for credentials)**
```bash
# From the backend directory
railway run poetry run python create_admin.py
```

**Method B: Using Railway Shell (Best for Windows/PowerShell)**

Open a shell with Railway environment variables, then set your admin credentials:

```powershell
# Open a shell with Railway environment variables
railway shell

# In the new shell, set environment variables (PowerShell syntax)
$env:ADMIN_EMAIL = "admin@example.com"
$env:ADMIN_PASSWORD = "your-secure-password-here"
$env:ADMIN_FIRST_NAME = "Admin"
$env:ADMIN_LAST_NAME = "User"

# Run the script (it will use production DATABASE_URL automatically)
poetry run python create_admin.py
```

**Method C: One-liner with Railway Run (Linux/macOS/Git Bash)**

For Unix-like shells (bash, zsh, Git Bash on Windows):

```bash
# From the backend directory
railway run bash -c "ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=securepass123 ADMIN_FIRST_NAME=Admin ADMIN_LAST_NAME=User poetry run python create_admin.py"
```

**Note for Windows PowerShell:** Use Method B (`railway shell`) as PowerShell's environment variable syntax doesn't work well with `railway run` in a single command.

#### Option 2: SSH into Railway Service Container

You can SSH directly into your running backend service and run the script there:

```bash
# First, link to your project
railway link

# SSH into your backend service
railway ssh

# Once inside the container, run:
poetry run python create_admin.py
```

**Note:** This requires your service to be running. If it's in serverless mode and sleeping, wake it up first by making a request to your API.

#### Option 3: Railway Database Dashboard (Not Recommended)

1. Go to Railway Dashboard → Your Database Service
2. Click "Connect" or "Query"
3. Use the SQL editor (but remember password hashing is complex - not recommended)

#### Option 4: Local Connection with Production DATABASE_URL

If you have the production database connection string:

```bash
# Set DATABASE_URL to production database (get this from Railway dashboard)
export DATABASE_URL="postgresql://user:pass@host:port/dbname"

# Run the script
poetry run python create_admin.py
```

**⚠️ Security Warning:** Be careful with this method - never commit production credentials to version control!

### Managing Admin Users via API (Recommended for Ongoing Management)

Once you have your first admin user created, you can manage admin status through the API endpoints. This is the **recommended approach** for production environments.

#### List All Users (Admin Only)
```bash
# Get all users (paginated)
curl -X GET "https://your-api.com/admin/users?page=1&limit=100" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

Response:
```json
{
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_admin": false,
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 100
}
```

#### Promote/Demote User to Admin (Admin Only)
```bash
# Promote a user to admin
curl -X PUT "https://your-api.com/admin/users/1/admin-status" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_admin": true}'

# Demote a user from admin
curl -X PUT "https://your-api.com/admin/users/1/admin-status" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_admin": false}'
```

**Security Features:**
- Requires admin authentication
- Prevents admins from removing their own admin status
- Returns proper error messages for invalid requests

**Best Practice:** Use these API endpoints instead of direct database access for ongoing admin management. This ensures:
- Proper authentication and authorization
- Audit trails (if you add logging)
- Consistent validation
- Better security

---

## Database Service Methods

The `DatabaseService` class provides these methods for data management:

### User Operations
- `create_user(user_data)` - Create a new user (passwords are hashed automatically)
- `get_user(user_id)` - Get user by ID
- `get_user_by_email(email)` - Get user by email
- `get_all_users(page, limit)` - Get all users with pagination (admin only)
- `update_user_admin_status(user_id, is_admin)` - Update admin status
- `verify_user_credentials(email, password)` - Verify login credentials

### Product Operations
- `create_product(product_data)` - Create a new product
- `get_product(product_id)` - Get product by ID
- `get_products(page, limit, category, search)` - Get products with filtering
- `update_product(product_id, product_data)` - Update a product
- `delete_product(product_id)` - Soft delete (sets is_available=False)

### Order Operations
- `create_order(order_data)` - Create a new order
- `get_order(order_id)` - Get order by ID
- `get_user_orders(user_id)` - Get all orders for a user
- `update_order_status(order_id, status)` - Update order status

---

## Security Notes

1. **Passwords:** Always use `DatabaseService.create_user()` which automatically hashes passwords. Never store plain text passwords.

2. **Admin Users:** Only create admin users through trusted scripts or the API. Never allow regular registration to create admin users.

3. **Production:** In production, prefer API endpoints over direct database access for better security and audit trails.

4. **Environment Variables:** Keep database credentials secure. Use `.env` files (not committed to git) or Railway's environment variables.

---

## Troubleshooting

### "User already exists"
- The script will offer to promote the existing user to admin
- Or use `update_user_admin_status()` method

### "Password too short"
- Minimum 8 characters required
- The script validates this automatically

### "Database connection error"
- Check your `DATABASE_URL` environment variable
- Ensure database is running and accessible
- For Railway, check the database service is running

### "Permission denied"
- Ensure you have write access to the database
- Check database user permissions
- For Railway, ensure you're using the correct database URL

---

## Quick Reference

```bash
# Create admin user
poetry run python create_admin.py

# Seed products
poetry run python seed_products.py

# Run database migrations
alembic upgrade head

# Check database connection
poetry run python -c "from app.database_config import engine; engine.connect(); print('Connected!')"
```


