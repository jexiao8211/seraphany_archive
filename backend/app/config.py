"""
Centralized configuration for the backend application
"""
import os
import json
from typing import Optional, Any
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./test.db",
        description="Database connection URL"
    )
    
    # Legacy field names for compatibility with existing .env
    DATABASE_URL: Optional[str] = Field(default=None, description="Legacy database URL field")
    SECRET_KEY: Optional[str] = Field(default=None, description="Legacy secret key field")
    DEBUG: Optional[bool] = Field(default=None, description="Legacy debug field")
    
    # JWT Configuration
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT token signing"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        description="JWT access token expiration in minutes"
    )
    
    # Upload Configuration
    upload_dir: str = Field(
        default="uploads",
        description="Directory for file uploads"
    )
    max_file_size: int = Field(
        default=5 * 1024 * 1024,  # 5MB
        description="Maximum file size in bytes"
    )
    allowed_file_types: set[str] = Field(
        default={'.jpg', '.jpeg', '.png', '.webp'},
        description="Allowed file extensions"
    )
    
    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"],
        description="Allowed CORS origins"
    )
    CORS_ORIGINS: Optional[str] = Field(
        default=None, 
        description="CORS origins as JSON string or comma-separated"
    )
    
    @model_validator(mode='after')
    @classmethod
    def parse_cors_origins_after_validation(cls, model: 'Settings') -> 'Settings':
        """Parse CORS_ORIGINS after validation and set cors_origins"""
        if model.CORS_ORIGINS and model.CORS_ORIGINS.strip():
            try:
                # Try parsing as JSON first
                parsed = json.loads(model.CORS_ORIGINS)
                if isinstance(parsed, list):
                    # Normalize origins to ensure they have protocols
                    model.cors_origins = [cls._normalize_origin(origin) for origin in parsed]
                    return model
            except (json.JSONDecodeError, TypeError, ValueError):
                # If not JSON, treat as comma-separated string
                origins = [origin.strip() for origin in model.CORS_ORIGINS.split(',') if origin.strip()]
                if origins:
                    # Normalize origins to ensure they have protocols
                    model.cors_origins = [cls._normalize_origin(origin) for origin in origins]
        return model
    
    def get_cors_origins(self) -> list[str]:
        """Get CORS origins, parsing from CORS_ORIGINS env var if provided"""
        if self.CORS_ORIGINS:
            try:
                # Try parsing as JSON first
                origins = json.loads(self.CORS_ORIGINS)
                if isinstance(origins, list):
                    return [self._normalize_origin(origin) for origin in origins]
            except (json.JSONDecodeError, TypeError):
                # If not JSON, try comma-separated
                origins = [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
                return [self._normalize_origin(origin) for origin in origins]
        
        # Normalize default origins too
        return [self._normalize_origin(origin) for origin in self.cors_origins]
    
    @staticmethod
    def _normalize_origin(origin: str) -> str:
        """
        Normalize CORS origin to ensure it has a protocol.
        CORS origins must match exactly what the browser sends in the Origin header,
        which always includes the protocol (http:// or https://).
        """
        if not origin or not isinstance(origin, str):
            return origin
        
        origin = origin.strip()
        
        # If origin already has protocol, return as-is
        if origin.startswith('http://') or origin.startswith('https://'):
            return origin
        
        # If no protocol, assume https:// for production domains
        # (localhost can stay as http:// for development)
        if 'localhost' in origin or '127.0.0.1' in origin:
            return f'http://{origin}'
        else:
            # For production domains, default to https://
            return f'https://{origin}'
    
    # Application Configuration
    app_name: str = Field(default="Storefront API", description="Seraphany")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True  # Make case-sensitive so CORS_ORIGINS doesn't map to cors_origins
        extra = "ignore"  # Ignore extra fields from environment


# Global settings instance
settings = Settings()


def get_database_url() -> str:
    """Get database URL with fallback"""
    # Use DATABASE_URL from .env if available, otherwise use database_url
    return settings.DATABASE_URL or settings.database_url


def get_jwt_secret() -> str:
    """Get JWT secret key"""
    # Use SECRET_KEY from .env if available, otherwise use jwt_secret_key
    return settings.SECRET_KEY or settings.jwt_secret_key


def get_upload_dir() -> str:
    """Get upload directory path"""
    return settings.upload_dir


def get_max_file_size() -> int:
    """Get maximum file size in bytes"""
    return settings.max_file_size


def get_allowed_file_types() -> set[str]:
    """Get allowed file types"""
    return settings.allowed_file_types


def get_debug_mode() -> bool:
    """Get debug mode setting"""
    # Use DEBUG from .env if available, otherwise use debug
    return settings.DEBUG if settings.DEBUG is not None else settings.debug

