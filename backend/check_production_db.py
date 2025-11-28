"""
Test script to verify production database connection
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load production environment variables
load_dotenv('.env.production')

# Get database URL
database_url = os.getenv('DATABASE_URL')

if not database_url:
    print("ERROR: DATABASE_URL not found in .env.production")
    print("Please make sure you've added DATABASE_URL to backend/.env.production")
    exit(1)

print(f"Testing connection to: {database_url[:30]}...")

try:
    # Create engine and test connection
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        # Test query
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("SUCCESS: Connection successful!")
        print(f"PostgreSQL version: {version}")
        
        # Check if we can list tables
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            print(f"Existing tables: {', '.join(tables)}")
        else:
            print("No tables found (database is empty - ready for migrations)")
            
except Exception as e:
    print(f"ERROR: Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check that your DATABASE_URL is correct")
    print("2. Make sure Railway database is running")
    print("3. Verify network connectivity")
    exit(1)

print("\nDatabase connection test complete!")
