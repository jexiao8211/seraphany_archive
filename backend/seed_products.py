"""
Seed script to add sample products to the database
Run this with: poetry run python seed_products.py (from backend directory)
"""
from app.database import DatabaseService

def seed_products():
    db = DatabaseService()
    
    products = [
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
    for product_data in products:
        product = db.create_product(product_data)
        print(f"[OK] Added: {product['name']}")
    
    print(f"\n[SUCCESS] Successfully added {len(products)} products!")

if __name__ == "__main__":
    seed_products()

