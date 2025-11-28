"""
FastAPI dependencies for authentication and database access
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from .auth import AuthService
from .database import DatabaseService
from .schemas import UserResponse

# Security scheme for JWT Bearer token
security = HTTPBearer(auto_error=False)


def get_database_service() -> DatabaseService:
    """Get database service instance"""
    return DatabaseService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: DatabaseService = Depends(get_database_service)
) -> UserResponse:
    """
    Dependency to get the current authenticated user from JWT token.
    Raises 401 if token is invalid or user not found.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Extract user ID from token
        user_id = AuthService.get_user_id_from_token(credentials.credentials)
        
        # Get user from database
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_admin=user.get("is_admin", False)
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: DatabaseService = Depends(get_database_service)
) -> Optional[UserResponse]:
    """
    Dependency to optionally get the current user.
    Returns None if no token provided, raises 401 if token is invalid.
    """
    if not credentials:
        return None
    
    try:
        user_id = AuthService.get_user_id_from_token(credentials.credentials)
        user = db.get_user(user_id)
        
        if not user:
            return None
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_admin=user.get("is_admin", False)
        )
    except Exception:
        return None


async def get_admin_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Dependency to get the current user and verify they are an admin.
    Raises 403 if user is not an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
