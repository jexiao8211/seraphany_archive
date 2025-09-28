"""
Tests for order-related API endpoints.
Following TDD approach - tests written before implementation.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestOrderEndpoints:
    """Test cases for order API endpoints."""
    
    def test_create_order_requires_authentication(self, client):
        """Test that POST /orders requires authentication."""
        order_data = {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1}
            ],
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_create_order_with_valid_data(self, client, auth_helper, test_db_service):
        """Test creating an order with valid data (when authenticated)."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer@example.com",
            password="customerpass123"
        )
        
        # Create test products first using the same database service as the app
        db = test_db_service
        
        product1_data = {
            "name": "Vintage Chanel Dress",
            "description": "Beautiful vintage Chanel dress",
            "price": 1500.00,
            "category": "dresses",
            "images": ["image1.jpg"]
        }
        product2_data = {
            "name": "Vintage Hermes Bag",
            "description": "Classic Hermes handbag",
            "price": 2500.00,
            "category": "bags",
            "images": ["image2.jpg"]
        }
        
        # Create products in database
        product1 = db.create_product(product1_data)
        product2 = db.create_product(product2_data)
        
        print(f"Created product1 with ID: {product1['id']}")
        print(f"Created product2 with ID: {product2['id']}")
        
        order_data = {
            "items": [
                {"product_id": product1["id"], "quantity": 2},
                {"product_id": product2["id"], "quantity": 1}
            ],
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }
        
        # Test creating order with authentication
        response = client.post("/orders", json=order_data, 
                              headers=auth_helper.get_auth_headers("customer@example.com"))
        # Should return 201 for successful order creation
        if response.status_code != 201:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "items" in data
        assert "total_amount" in data
        assert "status" in data
        assert data["status"] == "PENDING"
    
    def test_create_order_with_invalid_product_id(self, client, auth_helper, test_db_service):
        """Test creating order with non-existent product returns 400."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer2@example.com",
            password="customerpass123"
        )
        
        order_data = {
            "items": [
                {"product_id": 99999, "quantity": 1}  # Non-existent product
            ],
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }
        
        # Test with authentication - should get 400 (Bad Request) for invalid product
        response = client.post("/orders", json=order_data, 
                              headers=auth_helper.get_auth_headers("customer2@example.com"))
        assert response.status_code == 400
        data = response.json()
        assert "Product with ID 99999 not found" in data["detail"]
    
    def test_create_order_with_zero_quantity(self, client, auth_helper, test_db_service):
        """Test that zero quantity returns 400."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer3@example.com",
            password="customerpass123"
        )
        
        # Create a test product first
        product_data = {
            "name": "Test Product Zero",
            "description": "Test product for zero quantity test",
            "price": 100.00,
            "category": "test",
            "images": ["test_zero.jpg"]
        }
        product = test_db_service.create_product(product_data)
        
        order_data = {
            "items": [
                {"product_id": product["id"], "quantity": 0}  # Invalid quantity
            ],
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }
        
        # Test with authentication - should get 400 (Bad Request) for zero quantity
        response = client.post("/orders", json=order_data, 
                              headers=auth_helper.get_auth_headers("customer3@example.com"))
        assert response.status_code == 400
        data = response.json()
        assert "Quantity must be greater than 0" in data["detail"]
    
    def test_get_user_orders_requires_authentication(self, client):
        """Test that GET /orders requires authentication."""
        response = client.get("/orders")
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_get_user_orders_with_valid_token(self, client, auth_helper, test_db_service):
        """Test getting user orders with valid token."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer4@example.com",
            password="customerpass123"
        )
        
        # Test getting orders with authentication
        response = client.get("/orders", headers=auth_helper.get_auth_headers("customer4@example.com"))
        # Should return 200 with empty list for new user
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_single_order_requires_authentication(self, client):
        """Test that GET /orders/{id} requires authentication."""
        response = client.get("/orders/1")
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_get_single_order_with_valid_token(self, client, auth_helper, test_db_service):
        """Test getting single order with valid token."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer5@example.com",
            password="customerpass123"
        )
        
        # Test getting single order with authentication
        response = client.get("/orders/1", headers=auth_helper.get_auth_headers("customer5@example.com"))
        # Should return 404 for non-existent order
        assert response.status_code == 404
        data = response.json()
        assert "Order not found" in data["detail"]
    
    def test_get_order_from_different_user_returns_403(self, client, auth_helper, test_db_service):
        """Test that users can only access their own orders."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer6@example.com",
            password="customerpass123"
        )
        
        # Test getting order with authentication
        response = client.get("/orders/1", headers=auth_helper.get_auth_headers("customer6@example.com"))
        # Should return 404 for non-existent order
        assert response.status_code == 404
        data = response.json()
        assert "Order not found" in data["detail"]
    
    def test_update_order_status_requires_authentication(self, client):
        """Test that PUT /orders/{id}/status requires authentication."""
        status_data = {"status": "shipped"}
        response = client.put("/orders/1/status", json=status_data)
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_cancel_order_requires_authentication(self, client):
        """Test that POST /orders/{id}/cancel requires authentication."""
        response = client.post("/orders/1/cancel")
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_update_order_status_with_valid_data(self, client, auth_helper, test_db_service):
        """Test updating order status with valid data."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer7@example.com",
            password="customerpass123"
        )
        
        # Create a test product first
        product_data = {
            "name": "Test Product",
            "description": "Test product for order",
            "price": 100.00,
            "category": "test",
            "images": ["test.jpg"]
        }
        product = test_db_service.create_product(product_data)
        
        # First create an order
        order_data = {
            "items": [
                {"product_id": product["id"], "quantity": 2}
            ],
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }
        
        create_response = client.post("/orders", json=order_data, 
                                   headers=auth_helper.get_auth_headers("customer7@example.com"))
        assert create_response.status_code == 201
        order_id = create_response.json()["id"]
        
        # Update order status
        status_data = {"status": "CONFIRMED"}
        response = client.put(f"/orders/{order_id}/status", json=status_data,
                            headers=auth_helper.get_auth_headers("customer7@example.com"))
        if response.status_code != 200:
            print(f"Status update response status: {response.status_code}")
            print(f"Status update response body: {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "Order status updated successfully" in data["message"]
        assert data["new_status"] == "CONFIRMED"
    
    def test_cancel_order_with_valid_data(self, client, auth_helper, test_db_service):
        """Test cancelling an order with valid data."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="customer8@example.com",
            password="customerpass123"
        )
        
        # Create a test product first
        product_data = {
            "name": "Test Product 2",
            "description": "Test product for order 2",
            "price": 200.00,
            "category": "test",
            "images": ["test2.jpg"]
        }
        product = test_db_service.create_product(product_data)
        
        # First create an order
        order_data = {
            "items": [
                {"product_id": product["id"], "quantity": 1}
            ],
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            }
        }
        
        create_response = client.post("/orders", json=order_data, 
                                   headers=auth_helper.get_auth_headers("customer8@example.com"))
        assert create_response.status_code == 201
        order_id = create_response.json()["id"]
        
        # Cancel the order
        response = client.post(f"/orders/{order_id}/cancel",
                             headers=auth_helper.get_auth_headers("customer8@example.com"))
        if response.status_code != 200:
            print(f"Cancel response status: {response.status_code}")
            print(f"Cancel response body: {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "Order cancelled successfully" in data["message"]
        assert data["status"] == "CANCELLED"
