"""
Configuration settings for the Vintage Store backend
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/vintage_store_dev"
    )
    
    # Application Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vintage Store API"

# Global settings instance
settings = Settings()
