"""
Users router - handles admin user management operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from ..database import DatabaseService
from ..dependencies import get_database_service, get_admin_user
from ..schemas import UserResponse, AdminStatusUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=Dict[str, Any])
async def get_all_users(
    page: int = 1,
    limit: int = 100,
    current_user: UserResponse = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Get all users (admin only)."""
    try:
        users = db.get_all_users(page=page, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )


@router.put("/users/{user_id}/admin-status", response_model=UserResponse)
async def update_user_admin_status(
    user_id: int,
    admin_status: AdminStatusUpdate,
    current_user: UserResponse = Depends(get_admin_user),
    db: DatabaseService = Depends(get_database_service)
):
    """Update a user's admin status (admin only)."""
    try:
        # Prevent users from removing their own admin status
        if user_id == current_user.id and not admin_status.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot remove your own admin status"
            )
        
        updated_user = db.update_user_admin_status(user_id, admin_status.is_admin)
        
        return UserResponse(
            id=updated_user["id"],
            email=updated_user["email"],
            first_name=updated_user["first_name"],
            last_name=updated_user["last_name"],
            is_admin=updated_user["is_admin"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user admin status: {str(e)}"
        )

