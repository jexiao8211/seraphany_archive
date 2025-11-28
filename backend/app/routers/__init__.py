"""
Routers package - contains all API route handlers
"""
from .auth import router as auth_router
from .products import router as products_router
from .orders import router as orders_router
from .uploads import router as uploads_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "products_router",
    "orders_router",
    "uploads_router",
    "users_router",
]

