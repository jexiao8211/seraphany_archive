"""
Tests for user-related API endpoints.
Following TDD approach - tests written before implementation.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUserEndpoints:
    """Test cases for user API endpoints."""
    
    def test_register_user_with_valid_data(self):
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
    
    def test_register_user_with_existing_email(self):
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
    
    def test_register_user_with_invalid_email(self):
        """Test that invalid email format returns 422."""
        user_data = {
            "email": "invalid-email",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Pydantic validation error
    
    def test_register_user_with_weak_password(self):
        """Test that weak password returns 400."""
        user_data = {
            "email": "test@example.com",
            "password": "123",  # Too short
            "first_name": "John",
            "last_name": "Doe"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
    
    def test_login_with_valid_credentials(self):
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
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials returns 401."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_get_current_user_requires_authentication(self):
        """Test that GET /auth/me requires authentication."""
        response = client.get("/auth/me")
        assert response.status_code == 403
    
    def test_get_current_user_with_valid_token(self):
        """Test getting current user with valid token."""
        # This test will be updated once we implement JWT tokens
        # For now, we expect 403
        response = client.get("/auth/me")
        assert response.status_code == 403
    
    def test_logout_requires_authentication(self):
        """Test that POST /auth/logout requires authentication."""
        response = client.post("/auth/logout")
        assert response.status_code == 403
