"""
Authentication router - handles user registration, login, logout, and token management
"""
from fastapi import APIRouter, Depends, HTTPException, status

from ..database import DatabaseService
from ..auth import AuthService
from ..dependencies import get_database_service, get_current_user
from ..schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    TokenRefresh,
    MessageResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: DatabaseService = Depends(get_database_service)
):
    """Register a new user."""
    # Basic validation
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Check if user already exists
    existing_user = db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password
    }
    
    new_user = db.create_user(user_data)
    
    return UserResponse(
        id=new_user["id"],
        email=new_user["email"],
        first_name=new_user["first_name"],
        last_name=new_user["last_name"],
        is_admin=new_user.get("is_admin", False)
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    credentials: UserLogin,
    db: DatabaseService = Depends(get_database_service)
):
    """Login user and return JWT token."""
    # Verify user credentials
    user = db.verify_user_credentials(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create JWT token
    access_token = AuthService.create_access_token(data={"sub": str(user["id"])})
    
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get current user information."""
    return current_user


@router.post("/logout", response_model=MessageResponse)
async def logout_user(
    current_user: UserResponse = Depends(get_current_user)
):
    """Logout user."""
    # For JWT tokens, logout is handled client-side by removing the token
    # In a more sophisticated setup, you might maintain a blacklist of tokens
    return MessageResponse(message="Successfully logged out")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh):
    """Refresh JWT token."""
    try:
        # Verify the current token
        payload = AuthService.verify_token(token_data.refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Create new token
        access_token = AuthService.create_access_token(data={"sub": user_id})
        
        return TokenResponse(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

