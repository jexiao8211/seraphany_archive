"""
Authentication helper functions for tests
"""
from fastapi.testclient import TestClient
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import User


class AuthTestHelper:
    """Helper class for authentication in tests"""
    
    def __init__(self, client: TestClient, test_db: Optional[Session] = None):
        self.client = client
        self.test_db = test_db
        self._auth_tokens: Dict[str, str] = {}
    
    def register_user(self, email: str = "test@example.com", password: str = "testpass123", 
                     first_name: str = "Test", last_name: str = "User") -> Dict[str, Any]:
        """Register a new user and return user data"""
        user_data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        response = self.client.post("/auth/register", json=user_data)
        assert response.status_code == 201, f"Registration failed: {response.text}"
        return response.json()
    
    def login_user(self, email: str = "test@example.com", password: str = "testpass123") -> str:
        """Login a user and return JWT token"""
        login_data = {
            "email": email,
            "password": password
        }
        response = self.client.post("/auth/login", json=login_data)
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        token = data["access_token"]
        self._auth_tokens[email] = token
        return token
    
    def get_auth_headers(self, email: str = "test@example.com") -> Dict[str, str]:
        """Get authorization headers for a user"""
        if email not in self._auth_tokens:
            # Auto-login if token not available
            self.login_user(email)
        
        token = self._auth_tokens[email]
        return {"Authorization": f"Bearer {token}"}
    
    def create_authenticated_user(self, email: str = "test@example.com", 
                                 password: str = "testpass123",
                                 first_name: str = "Test", 
                                 last_name: str = "User") -> tuple[Dict[str, Any], str]:
        """Create a user, login, and return (user_data, token)"""
        user_data = self.register_user(email, password, first_name, last_name)
        token = self.login_user(email, password)
        return user_data, token
    
    def create_admin_user(self, email: str = "admin@example.com", 
                         password: str = "adminpass123",
                         first_name: str = "Admin", 
                         last_name: str = "User") -> tuple[Dict[str, Any], str]:
        """Create an admin user, login, and return (user_data, token)"""
        user_data = self.register_user(email, password, first_name, last_name)
        
        # Set is_admin to True in the database
        if self.test_db:
            user = self.test_db.query(User).filter(User.email == email).first()
            if user:
                user.is_admin = True
                self.test_db.commit()
        
        # Login AFTER setting admin status to get fresh token
        token = self.login_user(email, password)
        return user_data, token
    
    def make_authenticated_request(self, method: str, url: str, 
                                  email: str = "test@example.com", 
                                  json: Optional[Dict[str, Any]] = None,
                                  **kwargs) -> Any:
        """Make an authenticated request"""
        headers = self.get_auth_headers(email)
        if json:
            return self.client.request(method, url, json=json, headers=headers, **kwargs)
        else:
            return self.client.request(method, url, headers=headers, **kwargs)
    
    def test_auth_required(self, method: str, url: str, json: Optional[Dict[str, Any]] = None):
        """Test that an endpoint requires authentication"""
        if json:
            response = self.client.request(method, url, json=json)
        else:
            response = self.client.request(method, url)
        
        assert response.status_code == 401, f"Expected 401 (Unauthorized), got {response.status_code}: {response.text}"
        return response
    
    def test_invalid_token(self, method: str, url: str, json: Optional[Dict[str, Any]] = None):
        """Test that an invalid token returns 401"""
        headers = {"Authorization": "Bearer invalid_token"}
        if json:
            response = self.client.request(method, url, json=json, headers=headers)
        else:
            response = self.client.request(method, url, headers=headers)
        
        assert response.status_code == 401, f"Expected 401 (Unauthorized), got {response.status_code}: {response.text}"
        return response
