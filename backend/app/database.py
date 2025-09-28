"""
Database service for the Vintage Store
Handles all database operations using Prisma ORM
"""
from prisma import Prisma
from typing import List, Optional, Dict, Any
from decimal import Decimal
import asyncio

class DatabaseService:
    """Database service class for handling all database operations"""
    
    def __init__(self):
        self.prisma = Prisma()
        self._connected = False
    
    async def connect(self):
        """Connect to the database"""
        if not self._connected:
            await self.prisma.connect()
            self._connected = True
    
    async def disconnect(self):
        """Disconnect from the database"""
        if self._connected:
            await self.prisma.disconnect()
            self._connected = False
    
    # Product operations
    async def get_products(
        self, 
        page: int = 1, 
        limit: int = 10, 
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get products with optional filtering and pagination"""
        await self.connect()
        
        # Build where clause
        where_clause = {"isAvailable": True}
        if category:
            where_clause["category"] = category
        if search:
            where_clause["name"] = {"contains": search, "mode": "insensitive"}
        
        # Get total count
        total = await self.prisma.product.count(where=where_clause)
        
        # Get paginated results
        skip = (page - 1) * limit
        products = await self.prisma.product.find_many(
            where=where_clause,
            skip=skip,
            take=limit,
            order_by={"createdAt": "desc"}
        )
        
        return {
            "items": products,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    async def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get a single product by ID"""
        await self.connect()
        return await self.prisma.product.find_unique(where={"id": product_id})
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product"""
        await self.connect()
        return await self.prisma.product.create(data=product_data)
    
    async def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a product"""
        await self.connect()
        return await self.prisma.product.update(
            where={"id": product_id},
            data=product_data
        )
    
    async def delete_product(self, product_id: int) -> Dict[str, Any]:
        """Delete a product (soft delete by setting isAvailable to False)"""
        await self.connect()
        return await self.prisma.product.update(
            where={"id": product_id},
            data={"isAvailable": False}
        )
    
    # User operations
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        await self.connect()
        return await self.prisma.user.create(data=user_data)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        await self.connect()
        return await self.prisma.user.find_unique(where={"email": email})
    
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        await self.connect()
        return await self.prisma.user.find_unique(where={"id": user_id})
    
    # Order operations
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order"""
        await self.connect()
        return await self.prisma.order.create(data=order_data)
    
    async def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all orders for a user"""
        await self.connect()
        return await self.prisma.order.find_many(
            where={"userId": user_id},
            include={"items": {"include": {"product": True}}},
            order_by={"createdAt": "desc"}
        )
    
    async def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get a single order by ID"""
        await self.connect()
        return await self.prisma.order.find_unique(
            where={"id": order_id},
            include={"items": {"include": {"product": True}}, "user": True}
        )
    
    async def update_order_status(self, order_id: int, status: str) -> Dict[str, Any]:
        """Update order status"""
        await self.connect()
        return await self.prisma.order.update(
            where={"id": order_id},
            data={"status": status}
        )

# Global database service instance
db = DatabaseService()
