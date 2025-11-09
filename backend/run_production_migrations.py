"""
Script to run Alembic migrations on production database
Usage: poetry run python run_production_migrations.py
"""
import os
import sys
from dotenv import load_dotenv

# Load production environment variables
load_dotenv('.env.production')

# Set DATABASE_URL for Alembic
database_url = os.getenv('DATABASE_URL')
if not database_url:
    print("ERROR: DATABASE_URL not found in .env.production")
    sys.exit(1)

os.environ['DATABASE_URL'] = database_url

# Import and run Alembic upgrade
from alembic.config import Config
from alembic import command

# Get Alembic configuration
alembic_cfg = Config("alembic.ini")

# Run migrations
print("Running database migrations...")
print(f"Database: {database_url[:30]}...")
try:
    command.upgrade(alembic_cfg, "head")
    print("SUCCESS: All migrations applied!")
except Exception as e:
    print(f"ERROR: Migration failed: {e}")
    sys.exit(1)
