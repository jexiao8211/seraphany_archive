"""
Orders router - handles order creation, retrieval, and status management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..database import DatabaseService
from ..dependencies import get_database_service, get_current_user
from ..schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    OrderStatusResponse,
    OrderCancelResponse,
    ShippingAddress,
    UserResponse,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Create a new order (requires authentication)."""
    try:
        # Validate products exist and are available
        total_amount = 0.0
        order_items = []
        
        for item in order.items:
            # Get product details
            product = db.get_product(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with ID {item.product_id} not found"
                )
            
            if not product.get("is_available", True):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product['name']} is not available"
                )
            
            if item.quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quantity must be greater than 0"
                )
            
            # Calculate item total
            item_total = float(product["price"]) * item.quantity
            total_amount += item_total
            
            order_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(product["price"]),
                "product_name": product["name"]
            })
        
        # Create order data
        order_data = {
            "user_id": current_user.id,
            "total_amount": total_amount,
            "status": "PENDING",
            "shipping_address": order.shipping_address.model_dump(),
            "items": order_items
        }
        
        # Create order in database
        created_order = db.create_order(order_data)
        
        return OrderResponse(
            id=created_order["id"],
            user_id=created_order["user_id"],
            items=created_order["items"],
            total_amount=created_order["total_amount"],
            status=created_order["status"],
            shipping_address=ShippingAddress(**created_order["shipping_address"]),
            created_at=created_order["created_at"],
            updated_at=created_order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )


@router.get("", response_model=List[OrderResponse])
async def get_user_orders(
    current_user: UserResponse = Depends(get_current_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Get current user's orders (requires authentication)."""
    try:
        orders = db.get_user_orders(current_user.id)
        
        return [
            OrderResponse(
                id=order["id"],
                user_id=order["user_id"],
                items=order["items"],
                total_amount=order["total_amount"],
                status=order["status"],
                shipping_address=ShippingAddress(**order["shipping_address"]),
                created_at=order["created_at"],
                updated_at=order["updated_at"]
            ) for order in orders
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orders: {str(e)}"
        )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Get a specific order (requires authentication)."""
    try:
        order = db.get_order(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Check if the order belongs to the current user
        if order["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only view your own orders."
            )
        
        return OrderResponse(
            id=order["id"],
            user_id=order["user_id"],
            items=order["items"],
            total_amount=order["total_amount"],
            status=order["status"],
            shipping_address=ShippingAddress(**order["shipping_address"]),
            created_at=order["created_at"],
            updated_at=order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get order: {str(e)}"
        )


@router.put("/{order_id}/status", response_model=OrderStatusResponse)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Update order status (requires authentication)."""
    try:
        # First check if the order exists and belongs to the user
        order = db.get_order(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        if order["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only update your own orders."
            )
        
        # Validate status
        valid_statuses = ["PENDING", "CONFIRMED", "SHIPPED", "DELIVERED", "CANCELLED"]
        if status_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Update the order status
        updated_order = db.update_order_status(order_id, status_data.status)
        
        return OrderStatusResponse(
            message="Order status updated successfully",
            order_id=updated_order["id"],
            new_status=updated_order["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update order status: {str(e)}"
        )


@router.post("/{order_id}/cancel", response_model=OrderCancelResponse)
async def cancel_order(
    order_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Cancel an order (requires authentication)."""
    try:
        # First check if the order exists and belongs to the user
        order = db.get_order(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        if order["user_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only cancel your own orders."
            )
        
        # Check if order can be cancelled (not already delivered or cancelled)
        if order["status"] in ["DELIVERED", "CANCELLED"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel order with status: {order['status']}"
            )
        
        # Cancel the order
        updated_order = db.update_order_status(order_id, "CANCELLED")
        
        return OrderCancelResponse(
            message="Order cancelled successfully",
            order_id=updated_order["id"],
            status=updated_order["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel order: {str(e)}"
        )

