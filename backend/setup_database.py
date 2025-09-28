"""
Database setup script for the Vintage Store
This script helps set up the database and run migrations
"""
import asyncio
from prisma import Prisma
from config import settings

async def setup_database():
    """Set up the database with initial data"""
    print("🗄️ Setting up Vintage Store Database...")
    
    # Initialize Prisma client
    prisma = Prisma()
    await prisma.connect()
    
    try:
        print("✅ Connected to database successfully!")
        
        # Create some sample products for development
        sample_products = [
            {
                "name": "Vintage Chanel Dress",
                "description": "Beautiful vintage Chanel dress from the 1980s",
                "price": 1500.00,
                "category": "dresses",
                "images": ["https://example.com/chanel-dress-1.jpg", "https://example.com/chanel-dress-2.jpg"],
                "isAvailable": True
            },
            {
                "name": "Vintage Hermes Bag",
                "description": "Classic Hermes handbag in excellent condition",
                "price": 2500.00,
                "category": "bags",
                "images": ["https://example.com/hermes-bag-1.jpg"],
                "isAvailable": True
            },
            {
                "name": "Vintage Louis Vuitton Shoes",
                "description": "Elegant Louis Vuitton heels from the 1990s",
                "price": 800.00,
                "category": "shoes",
                "images": ["https://example.com/lv-shoes-1.jpg"],
                "isAvailable": True
            },
            {
                "name": "Vintage Dior Scarf",
                "description": "Silk Dior scarf with classic pattern",
                "price": 300.00,
                "category": "accessories",
                "images": ["https://example.com/dior-scarf-1.jpg"],
                "isAvailable": True
            }
        ]
        
        print("📦 Adding sample products...")
        for product_data in sample_products:
            await prisma.product.create(data=product_data)
            print(f"  ✅ Added: {product_data['name']}")
        
        print("🎉 Database setup completed successfully!")
        print(f"📊 Added {len(sample_products)} sample products")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        raise
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    asyncio.run(setup_database())
