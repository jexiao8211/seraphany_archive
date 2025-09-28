"""
Tests for user-related API endpoints.
Following TDD approach - tests written before implementation.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
# from app.database import db  # We'll use test_db_service instead
from app.models import User


class TestUserEndpoints:
    """Test cases for user API endpoints."""
    
    def test_register_user_with_valid_data(self, client, test_db):
        """Test user registration with valid data."""
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "first_name" in data
        assert "last_name" in data
        assert "password" not in data  # Password should not be returned
    
    def test_register_user_with_existing_email(self, client, test_db):
        """Test that registering with existing email returns 400."""
        user_data = {
            "email": "existing@example.com",
            "password": "securepassword123",
            "first_name": "Jane",
            "last_name": "Doe"
        }
        # First registration should succeed
        response1 = client.post("/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        response2 = client.post("/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "email" in response2.json()["detail"].lower()
    
    def test_register_user_with_invalid_email(self, client):
        """Test that invalid email format returns 422."""
        user_data = {
            "email": "invalid-email",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Pydantic validation error
    
    def test_register_user_with_weak_password(self, client):
        """Test that weak password returns 400."""
        user_data = {
            "email": "test@example.com",
            "password": "123",  # Too short
            "first_name": "John",
            "last_name": "Doe"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
    
    def test_login_with_valid_credentials(self, client):
        """Test login with valid credentials."""
        # First register a user
        user_data = {
            "email": "login@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
        client.post("/auth/register", json=user_data)
        
        # Then login
        login_data = {
            "email": "login@example.com",
            "password": "securepassword123"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        # Verify it's a real JWT token (not mock)
        assert data["access_token"] != "mock_jwt_token"
    
    def test_login_with_invalid_credentials(self, client):
        """Test login with invalid credentials returns 401."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_get_current_user_requires_authentication(self, client):
        """Test that GET /auth/me requires authentication."""
        response = client.get("/auth/me")
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_get_current_user_with_valid_token(self, client, auth_helper):
        """Test getting current user with valid token."""
        # Create and login a user
        user_data, token = auth_helper.create_authenticated_user(
            email="me@example.com",
            password="testpass123"
        )
        
        # Test /auth/me with valid token
        response = client.get("/auth/me", headers=auth_helper.get_auth_headers("me@example.com"))
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert "id" in data
    
    def test_logout_requires_authentication(self, client):
        """Test that POST /auth/logout requires authentication."""
        response = client.post("/auth/logout")
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_logout_with_valid_token(self, client, auth_helper):
        """Test logout with valid token."""
        # Create and login a user
        user_data, token = auth_helper.create_authenticated_user(
            email="logout@example.com",
            password="testpass123"
        )
        
        # Test logout with valid token
        response = client.post("/auth/logout", headers=auth_helper.get_auth_headers("logout@example.com"))
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "logged out" in data["message"].lower()
    
    def test_token_refresh(self, client, auth_helper):
        """Test token refresh functionality."""
        # Create and login a user
        user_data, token = auth_helper.create_authenticated_user(
            email="refresh@example.com",
            password="testpass123"
        )
        
        # Test token refresh
        refresh_data = {"refresh_token": token}
        response = client.post("/auth/refresh", json=refresh_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        # The token should be valid (may be same if generated at same time)
        assert len(data["access_token"]) > 0
    
    def test_invalid_token_returns_401(self, client):
        """Test that invalid token returns 401."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
