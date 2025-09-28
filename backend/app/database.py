"""
Database service for the Vintage Store
Handles all database operations using SQLAlchemy ORM
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from decimal import Decimal
from .models import User, Product, Order, OrderItem, OrderStatus
from .database_config import SessionLocal
from .auth import AuthService
import json

class DatabaseService:
    """Database service class for handling all database operations"""
    
    def __init__(self):
        pass
    
    def get_session(self) -> Session:
        """Get database session"""
        return SessionLocal()
    
    # Product operations
    def get_products(
        self, 
        page: int = 1, 
        limit: int = 10, 
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get products with optional filtering and pagination"""
        with self.get_session() as session:
            # Build query
            query = select(Product).where(Product.is_available == True)
            
            if category:
                query = query.where(Product.category == category)
            if search:
                query = query.where(Product.name.ilike(f"%{search}%"))
            
            # Get total count
            count_query = select(func.count(Product.id)).where(Product.is_available == True)
            if category:
                count_query = count_query.where(Product.category == category)
            if search:
                count_query = count_query.where(Product.name.ilike(f"%{search}%"))
            
            total_result = session.execute(count_query)
            total = total_result.scalar()
            
            # Get paginated results
            offset = (page - 1) * limit
            query = query.order_by(Product.created_at.desc()).offset(offset).limit(limit)
            
            result = session.execute(query)
            products = result.scalars().all()
            
            # Convert to dict format
            products_data = []
            for product in products:
                product_dict = {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": float(product.price),
                    "category": product.category,
                    "images": product.get_images(),
                    "isAvailable": product.is_available,
                    "createdAt": product.created_at.isoformat(),
                    "updatedAt": product.updated_at.isoformat()
                }
                products_data.append(product_dict)
            
            return {
                "items": products_data,
                "total": total,
                "page": page,
                "limit": limit
            }
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get a single product by ID"""
        with self.get_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = session.execute(query)
            product = result.scalar_one_or_none()
            
            if not product:
                return None
            
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                "images": product.get_images(),
                "isAvailable": product.is_available,
                "createdAt": product.created_at.isoformat(),
                "updatedAt": product.updated_at.isoformat()
            }
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product"""
        with self.get_session() as session:
            # Handle images list
            images = product_data.pop("images", [])
            
            product = Product(**product_data)
            product.set_images(images)
            
            session.add(product)
            session.commit()
            session.refresh(product)
            
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                "images": product.get_images(),
                "isAvailable": product.is_available,
                "createdAt": product.created_at.isoformat(),
                "updatedAt": product.updated_at.isoformat()
            }
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a product"""
        with self.get_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = session.execute(query)
            product = result.scalar_one_or_none()
            
            if not product:
                raise ValueError("Product not found")
            
            # Handle images if provided
            if "images" in product_data:
                product.set_images(product_data.pop("images"))
            
            # Update other fields
            for key, value in product_data.items():
                setattr(product, key, value)
            
            session.commit()
            session.refresh(product)
            
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                "images": product.get_images(),
                "isAvailable": product.is_available,
                "createdAt": product.created_at.isoformat(),
                "updatedAt": product.updated_at.isoformat()
            }
    
    def delete_product(self, product_id: int) -> Dict[str, Any]:
        """Delete a product (soft delete by setting isAvailable to False)"""
        with self.get_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = session.execute(query)
            product = result.scalar_one_or_none()
            
            if not product:
                raise ValueError("Product not found")
            
            product.is_available = False
            session.commit()
            session.refresh(product)
            
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                "images": product.get_images(),
                "isAvailable": product.is_available,
                "createdAt": product.created_at.isoformat(),
                "updatedAt": product.updated_at.isoformat()
            }
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with hashed password"""
        with self.get_session() as session:
            # Hash the password before storing
            hashed_password = AuthService.get_password_hash(user_data["password"])
            user_data["password"] = hashed_password
            
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with self.get_session() as session:
            query = select(User).where(User.email == email)
            result = session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "password": user.password,
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        with self.get_session() as session:
            query = select(User).where(User.id == user_id)
            result = session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
    
    def verify_user_credentials(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify user credentials and return user data if valid"""
        with self.get_session() as session:
            query = select(User).where(User.email == email)
            result = session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            # Verify password
            if not AuthService.verify_password(password, user.password):
                return None
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
    
    # Order operations
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order with items"""
        with self.get_session() as session:
            # Handle shipping address and items
            shipping_address = order_data.pop("shipping_address", None)
            items = order_data.pop("items", [])
            
            # Create the order
            order = Order(**order_data)
            if shipping_address:
                order.set_shipping_address(shipping_address)
            
            session.add(order)
            session.flush()  # Get the order ID without committing
            
            # Create order items
            order_items = []
            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    product_name=item["product_name"]
                )
                session.add(order_item)
                order_items.append({
                    "id": order_item.id,
                    "product_id": order_item.product_id,
                    "quantity": order_item.quantity,
                    "price": float(order_item.price),
                    "product_name": order_item.product_name
                })
            
            session.commit()
            session.refresh(order)
            
            return {
                "id": order.id,
                "userId": order.user_id,
                "totalAmount": float(order.total_amount),
                "status": order.status,
                "shippingAddress": order.get_shipping_address(),
                "items": order_items,
                "createdAt": order.created_at.isoformat(),
                "updatedAt": order.updated_at.isoformat()
            }
    
    def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all orders for a user"""
        with self.get_session() as session:
            query = select(Order).where(Order.user_id == user_id).options(
                selectinload(Order.items)
            ).order_by(Order.created_at.desc())
            
            result = session.execute(query)
            orders = result.scalars().all()
            
            orders_data = []
            for order in orders:
                items_data = []
                for item in order.items:
                    items_data.append({
                        "id": item.id,
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price": float(item.price),
                        "product_name": item.product_name
                    })
                
                orders_data.append({
                    "id": order.id,
                    "userId": order.user_id,
                    "totalAmount": float(order.total_amount),
                    "status": order.status,
                    "shippingAddress": order.get_shipping_address(),
                    "items": items_data,
                    "createdAt": order.created_at.isoformat(),
                    "updatedAt": order.updated_at.isoformat()
                })
            
            return orders_data
    
    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get a single order by ID"""
        with self.get_session() as session:
            query = select(Order).where(Order.id == order_id).options(
                selectinload(Order.items),
                selectinload(Order.user)
            )
            
            result = session.execute(query)
            order = result.scalar_one_or_none()
            
            if not order:
                return None
            
            items_data = []
            for item in order.items:
                items_data.append({
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "product_name": item.product_name
                })
            
            return {
                "id": order.id,
                "userId": order.user_id,
                "totalAmount": float(order.total_amount),
                "status": order.status,
                "shippingAddress": order.get_shipping_address(),
                "items": items_data,
                "user": {
                    "id": order.user.id,
                    "email": order.user.email,
                    "firstName": order.user.first_name,
                    "lastName": order.user.last_name
                },
                "createdAt": order.created_at.isoformat(),
                "updatedAt": order.updated_at.isoformat()
            }
    
    
    def update_order_status(self, order_id: int, status: str) -> Dict[str, Any]:
        """Update order status"""
        with self.get_session() as session:
            query = select(Order).where(Order.id == order_id)
            result = session.execute(query)
            order = result.scalar_one_or_none()
            
            if not order:
                raise ValueError("Order not found")
            
            order.status = status
            session.commit()
            session.refresh(order)
            
            return {
                "id": order.id,
                "userId": order.user_id,
                "totalAmount": float(order.total_amount),
                "status": order.status,
                "shippingAddress": order.get_shipping_address(),
                "createdAt": order.created_at.isoformat(),
                "updatedAt": order.updated_at.isoformat()
            }

# Global database service instance
db = DatabaseService()