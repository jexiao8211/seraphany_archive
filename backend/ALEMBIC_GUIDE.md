# Alembic Migration Guide

This guide explains how to use Alembic for database migrations in the Vintage Store project.

## What is Alembic?

Alembic is a lightweight database migration tool for SQLAlchemy. It helps you:
- **Track schema changes** over time
- **Apply migrations** to different environments
- **Rollback changes** if needed
- **Collaborate** with team members on database changes

## Project Setup

Our Alembic is already configured in the `backend/` directory with:
- `alembic.ini` - Configuration file
- `alembic/` - Migration scripts directory
- `alembic/env.py` - Environment configuration
- `alembic/versions/` - Migration files

## Basic Commands

### 1. Check Current Status
```bash
cd backend
poetry run alembic current
```
Shows which migration is currently applied.

### 2. View Migration History
```bash
poetry run alembic history --verbose
```
Shows all migrations and their status.

### 3. Check for Pending Migrations
```bash
poetry run alembic heads
```
Shows the latest migration version.

## Creating Migrations

### Auto-Generate Migration (Recommended)
```bash
# Generate migration based on model changes
poetry run alembic revision --autogenerate -m "Description of changes"
```

**Example:**
```bash
poetry run alembic revision --autogenerate -m "Add user profile fields"
```

### Manual Migration
```bash
# Create empty migration file
poetry run alembic revision -m "Description of changes"
```

## Applying Migrations

### Apply All Pending Migrations
```bash
poetry run alembic upgrade head
```

### Apply Specific Migration
```bash
# Apply up to a specific revision
poetry run alembic upgrade <revision_id>
```

### Apply One Migration at a Time
```bash
poetry run alembic upgrade +1
```

## Rolling Back Migrations

### Rollback to Previous Migration
```bash
poetry run alembic downgrade -1
```

### Rollback to Specific Migration
```bash
poetry run alembic downgrade <revision_id>
```

### Rollback All Migrations
```bash
poetry run alembic downgrade base
```

## Common Workflows

### 1. Adding a New Field

**Step 1:** Update your model in `app/models.py`
```python
class User(Base):
    # ... existing fields ...
    phone_number = Column(String, nullable=True)  # New field
```

**Step 2:** Generate migration
```bash
poetry run alembic revision --autogenerate -m "Add phone number to users"
```

**Step 3:** Review the generated migration file
```python
# In alembic/versions/xxx_add_phone_number_to_users.py
def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
```

**Step 4:** Apply the migration
```bash
poetry run alembic upgrade head
```

### 2. Removing a Field

**Step 1:** Remove from model
```python
class User(Base):
    # ... other fields ...
    # phone_number = Column(String, nullable=True)  # Remove this line
```

**Step 2:** Generate migration
```bash
poetry run alembic revision --autogenerate -m "Remove phone number from users"
```

**Step 3:** Apply migration
```bash
poetry run alembic upgrade head
```

### 3. Adding a New Table

**Step 1:** Create new model
```python
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**Step 2:** Generate migration
```bash
poetry run alembic revision --autogenerate -m "Add categories table"
```

**Step 3:** Apply migration
```bash
poetry run alembic upgrade head
```

### 4. Adding Foreign Key Relationship

**Step 1:** Update models
```python
class Product(Base):
    # ... existing fields ...
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="products")

class Category(Base):
    # ... existing fields ...
    products = relationship("Product", back_populates="category")
```

**Step 2:** Generate and apply migration
```bash
poetry run alembic revision --autogenerate -m "Add category relationship to products"
poetry run alembic upgrade head
```

## Environment-Specific Operations

### Development Environment
```bash
# Make sure you're in the backend directory
cd backend

# Check current status
poetry run alembic current

# Apply all migrations
poetry run alembic upgrade head
```

### Production Environment
```bash
# Always backup before migrations in production!
# Apply migrations
poetry run alembic upgrade head

# Verify the migration was applied
poetry run alembic current
```

### Testing Environment
```bash
# Tests use in-memory SQLite, so migrations aren't needed
# But you can still test migration scripts
poetry run alembic upgrade head
```

## Troubleshooting

### 1. Migration Conflicts
If you have conflicts with other developers:

```bash
# Check current status
poetry run alembic current

# See what migrations are available
poetry run alembic heads

# Merge conflicts if needed
poetry run alembic merge -m "Merge migrations" <revision1> <revision2>
```

### 2. Failed Migration
If a migration fails:

```bash
# Check the error message
# Fix the issue in the migration file
# Then retry
poetry run alembic upgrade head
```

### 3. Database Out of Sync
If your database is out of sync:

```bash
# Check what migrations are applied
poetry run alembic current

# See what should be applied
poetry run alembic heads

# Apply missing migrations
poetry run alembic upgrade head
```

### 4. Manual Database Changes
If you made manual database changes:

```bash
# Mark the current state as the latest migration
poetry run alembic stamp head
```

## Best Practices

### 1. Always Review Generated Migrations
```bash
# Generate migration
poetry run alembic revision --autogenerate -m "Add new field"

# Review the generated file in alembic/versions/
# Make sure it looks correct before applying
```

### 2. Use Descriptive Migration Messages
```bash
# Good
poetry run alembic revision --autogenerate -m "Add user email verification"

# Bad
poetry run alembic revision --autogenerate -m "Update"
```

### 3. Test Migrations
```bash
# Test the migration
poetry run alembic upgrade head

# Test rollback
poetry run alembic downgrade -1

# Apply again
poetry run alembic upgrade head
```

### 4. Backup Before Production Migrations
```bash
# Always backup your production database before applying migrations
pg_dump your_database > backup.sql

# Then apply migrations
poetry run alembic upgrade head
```

## Migration File Structure

Each migration file has this structure:

```python
"""Add user phone number

Revision ID: abc123
Revises: def456
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123'
down_revision = 'def456'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Apply the migration"""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    """Rollback the migration"""
    op.drop_column('users', 'phone_number')
```

## Common Migration Operations

### Adding Columns
```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
```

### Removing Columns
```python
def upgrade() -> None:
    op.drop_column('users', 'phone_number')

def downgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
```

### Adding Tables
```python
def upgrade() -> None:
    op.create_table('categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('categories')
```

### Adding Indexes
```python
def upgrade() -> None:
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
```

### Adding Foreign Keys
```python
def upgrade() -> None:
    op.add_column('products', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_products_category', 'products', 'categories', ['category_id'], ['id'])

def downgrade() -> None:
    op.drop_constraint('fk_products_category', 'products', type_='foreignkey')
    op.drop_column('products', 'category_id')
```

## Integration with Our Project

### Current Setup
Our project uses Alembic with:
- **PostgreSQL** for production
- **SQLite** for testing
- **Snake_case** column naming
- **Context managers** for session management

### Environment Variables
Make sure your `.env` file has:
```bash
DATABASE_URL=postgresql://user:password@localhost/vintage_store
```

### Running Migrations
```bash
# Navigate to backend directory
cd backend

# Apply all migrations
poetry run alembic upgrade head

# Check status
poetry run alembic current
```

## Advanced Topics

### Custom Migration Logic
Sometimes you need custom logic in migrations:

```python
def upgrade() -> None:
    # Add the column
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))
    
    # Populate the column with existing data
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET full_name = first_name || ' ' || last_name"
    )
    
    # Make it non-nullable
    op.alter_column('users', 'full_name', nullable=False)
```

### Data Migrations
For data changes (not just schema):

```python
def upgrade() -> None:
    # Update existing data
    connection = op.get_bind()
    connection.execute(
        "UPDATE products SET category = 'vintage' WHERE category IS NULL"
    )
```

### Conditional Migrations
For environment-specific changes:

```python
def upgrade() -> None:
    # Only run in development
    if os.getenv('ENVIRONMENT') == 'development':
        op.add_column('users', sa.Column('debug_info', sa.String(), nullable=True))
```

This guide should help you manage database migrations effectively in your Vintage Store project! 🚀
