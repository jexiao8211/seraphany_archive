"""
Seed script to add sample products to the database
Run this with: poetry run python seed_products.py (from backend directory)
"""
from app.database_config import SessionLocal
from app.crud import product as product_crud
from app.schemas import ProductCreate

def seed_products():
    db = SessionLocal()
    try:
        products_data = [
            {
                "name": "Vintage Floral Dress",
                "description": "Beautiful 1960s floral print dress in excellent condition",
                "price": 89.99,
                "category": "dresses",
                "images": ["https://placehold.co/400x400/e8d5c4/8b4513?text=Floral+Dress"],
                "is_available": True
            },
            {
                "name": "Classic Leather Handbag",
                "description": "Genuine leather handbag from the 1980s",
                "price": 125.00,
                "category": "bags",
                "images": ["https://placehold.co/400x400/c9b8a8/5d4e37?text=Leather+Bag"],
                "is_available": True
            },
            {
                "name": "Retro Sunglasses",
                "description": "Cat-eye sunglasses from the 1950s",
                "price": 45.00,
                "category": "accessories",
                "images": ["https://placehold.co/400x400/f5e6d3/333333?text=Sunglasses"],
                "is_available": True
            },
            {
                "name": "Vintage High Heels",
                "description": "Classic black heels from the 1970s",
                "price": 65.00,
                "category": "shoes",
                "images": ["https://placehold.co/400x400/d4b896/8b0000?text=Heels"],
                "is_available": True
            },
            {
                "name": "Bohemian Maxi Dress",
                "description": "Flowing maxi dress with intricate embroidery",
                "price": 95.00,
                "category": "dresses",
                "images": ["https://placehold.co/400x400/f0e5d8/654321?text=Maxi+Dress"],
                "is_available": True
            },
            {
                "name": "Pearl Necklace",
                "description": "Elegant strand of pearls from the 1940s",
                "price": 150.00,
                "category": "accessories",
                "images": ["https://placehold.co/400x400/faf0e6/daa520?text=Pearl+Necklace"],
                "is_available": True
            },
        ]
        
        print("Adding sample products...")
        for p_data in products_data:
            # Create Pydantic model
            # ProductCreate schema doesn't have is_available, but logic sets it to True.
            # Actually ProductCreate has ProductBase which has name, description, price, category, images.
            # is_available is in Product model (DB) and Product schema (Response).
            product_create = ProductCreate(
                name=p_data["name"],
                description=p_data["description"],
                price=p_data["price"],
                category=p_data["category"],
                images=p_data["images"]
            )
            
            product = product_crud.create_product(db, product_create)
            print(f"[OK] Added: {product.name}")
        
        print(f"\n[SUCCESS] Successfully added {len(products_data)} products!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
