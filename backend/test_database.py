"""
Test script to verify database setup
"""
import asyncio
from app.database import db

async def test_database_connection():
    """Test database connection and basic operations"""
    print("🧪 Testing database connection...")
    
    try:
        # Test connection
        await db.connect()
        print("✅ Database connection successful!")
        
        # Test getting products (should work even if empty)
        products = await db.get_products()
        print(f"✅ Products query successful! Found {products['total']} products")
        
        # Test getting a non-existent product
        product = await db.get_product(999)
        print(f"✅ Product query successful! Result: {product}")
        
        print("🎉 Database setup is working correctly!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print("💡 Make sure PostgreSQL is running and the database exists")
        print("💡 Check your DATABASE_URL in the .env file")
        raise
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(test_database_connection())
