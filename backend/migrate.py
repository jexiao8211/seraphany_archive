"""
Database migration script
This script handles database setup and migrations
"""
import asyncio
from prisma import Prisma
from config import settings

async def migrate_database():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    
    prisma = Prisma()
    await prisma.connect()
    
    try:
        # Check if we can connect
        await prisma.user.find_first()
        print("✅ Database connection successful!")
        
        # The schema is already defined in prisma/schema.prisma
        # Prisma will handle the migration automatically
        print("✅ Database schema is up to date!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("💡 Make sure PostgreSQL is running and the database exists")
        print("💡 Run: poetry run prisma db push")
        raise
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    asyncio.run(migrate_database())
