# Database Setup Guide

This guide will help you set up PostgreSQL and Prisma for the Vintage Store project.

## Prerequisites

1. **PostgreSQL**: Install PostgreSQL on your system
2. **Python**: Python 3.8+ with Poetry
3. **Prisma**: Already installed via Poetry

## Step 1: Install PostgreSQL

### Windows
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set for the `postgres` user

### macOS
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 2: Create Database

1. **Connect to PostgreSQL**:
   ```bash
   psql -U postgres
   ```

2. **Create the database**:
   ```sql
   CREATE DATABASE vintage_store_dev;
   \q
   ```

## Step 3: Configure Environment

1. **Create a `.env` file** in the backend directory:
   ```bash
   # Copy the example
   cp .example_env .env
   ```

2. **Update the DATABASE_URL** in `.env`:
   ```
   DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/vintage_store_dev"
   ```
   Replace `YOUR_PASSWORD` with your PostgreSQL password.

## Step 4: Run Database Migrations

1. **Generate Prisma client**:
   ```bash
   poetry run prisma generate
   ```

2. **Push the schema to database**:
   ```bash
   poetry run prisma db push
   ```

3. **Set up sample data**:
   ```bash
   poetry run python setup_database.py
   ```

## Step 5: Verify Setup

1. **Check database connection**:
   ```bash
   poetry run prisma studio
   ```
   This opens a web interface to view your data.

2. **Run tests**:
   ```bash
   poetry run pytest
   ```

## Database Schema

Our database includes these models:

- **User**: Customer accounts
- **Product**: Vintage items for sale
- **Order**: Customer purchases
- **OrderItem**: Individual items in orders

## Troubleshooting

### Connection Issues
- Check if PostgreSQL is running
- Verify the DATABASE_URL format
- Ensure the database exists

### Permission Issues
- Make sure the postgres user has access to the database
- Check firewall settings

### Prisma Issues
- Run `poetry run prisma generate` after schema changes
- Use `poetry run prisma db push` to sync schema

## Development Workflow

1. **Make schema changes** in `prisma/schema.prisma`
2. **Push changes**: `poetry run prisma db push`
3. **Generate client**: `poetry run prisma generate`
4. **Update code** to use new schema
5. **Test changes**: `poetry run pytest`

## Production Deployment

For production, you'll need to:
1. Set up a production PostgreSQL database
2. Update the DATABASE_URL in your deployment environment
3. Run migrations: `poetry run prisma db push`
4. Set up proper security and backups
