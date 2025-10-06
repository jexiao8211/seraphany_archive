"""
Tests for product-related API endpoints.
Following TDD approach - tests written before implementation.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
# from app.database import db  # We'll use test_db_service instead
from app.models import Product


class TestProductEndpoints:
    """Test cases for product API endpoints."""
    
    def test_get_products_returns_list(self, client, test_db):
        """Test that GET /products returns paginated products with metadata."""
        # Add some test products
        test_products = [
            Product(name="Test Product 1", description="Test Description 1", 
                   price=100.00, category="test", is_available=True),
            Product(name="Test Product 2", description="Test Description 2", 
                   price=200.00, category="test", is_available=True)
        ]
        
        for product in test_products:
            test_db.add(product)
        test_db.commit()
        
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        # Should return paginated response with metadata
        assert isinstance(data, dict)
        assert "items" in data
        assert "page" in data
        assert "limit" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) == 2
        assert data["total"] == 2
    
    def test_get_products_with_pagination(self, client, test_db):
        """Test that GET /products supports pagination."""
        # Add test products
        test_products = [
            Product(name="Test Product 1", description="Test Description 1", 
                   price=100.00, category="test", is_available=True),
            Product(name="Test Product 2", description="Test Description 2", 
                   price=200.00, category="test", is_available=True)
        ]
        
        for product in test_products:
            test_db.add(product)
        test_db.commit()
        
        response = client.get("/products?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
    
    def test_get_products_with_category_filter(self, client, test_db):
        """Test that GET /products filters by category."""
        # Add test products with different categories
        test_products = [
            Product(name="Dress 1", description="Test Dress", 
                   price=100.00, category="dresses", is_available=True),
            Product(name="Bag 1", description="Test Bag", 
                   price=200.00, category="bags", is_available=True)
        ]
        
        for product in test_products:
            test_db.add(product)
        test_db.commit()
        
        response = client.get("/products?category=dresses")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["category"] == "dresses"
    
    def test_get_products_with_search(self, client, test_db):
        """Test that GET /products supports search functionality."""
        # Add test products
        test_products = [
            Product(name="Vintage Dress", description="Beautiful vintage dress", 
                   price=100.00, category="dresses", is_available=True),
            Product(name="Modern Bag", description="Modern handbag", 
                   price=200.00, category="bags", is_available=True)
        ]
        
        for product in test_products:
            test_db.add(product)
        test_db.commit()
        
        response = client.get("/products?search=vintage")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert "vintage" in data["items"][0]["name"].lower()
    
    def test_get_single_product(self, client, test_db):
        """Test that GET /products/{id} returns a single product."""
        # Add a test product
        test_product = Product(name="Test Product", description="Test Description", 
                             price=100.00, category="test", is_available=True)
        test_db.add(test_product)
        test_db.commit()
        
        response = client.get("/products/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "price" in data
        assert "description" in data
    
    def test_get_nonexistent_product_returns_404(self, client, test_db):
        """Test that GET /products/{id} returns 404 for non-existent product."""
        response = client.get("/products/99999")
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_create_product_requires_authentication(self, client):
        """Test that POST /products requires authentication."""
        product_data = {
            "name": "Vintage Chanel Dress",
            "description": "Beautiful vintage Chanel dress",
            "price": 1500.00,
            "category": "dresses",
            "images": ["image1.jpg", "image2.jpg"]
        }
        response = client.post("/products", json=product_data)
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_create_product_with_valid_data(self, client, auth_helper):
        """Test creating a product with valid data (when authenticated)."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="admin@example.com",
            password="adminpass123"
        )
        
        product_data = {
            "name": "Vintage Chanel Dress",
            "description": "Beautiful vintage Chanel dress",
            "price": 1500.00,
            "category": "dresses",
            "images": ["image1.jpg", "image2.jpg"]
        }
        
        # Test creating product with authentication
        response = client.post("/products", json=product_data, 
                              headers=auth_helper.get_auth_headers("admin@example.com"))
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == "Vintage Chanel Dress"
        assert data["description"] == "Beautiful vintage Chanel dress"
        assert data["price"] == 1500.00
        assert data["category"] == "dresses"
        assert len(data["images"]) == 2
        assert data["is_available"] == True
    
    def test_update_product_requires_authentication(self, client):
        """Test that PUT /products/{id} requires authentication."""
        product_data = {
            "name": "Updated Vintage Chanel Dress",
            "description": "Updated description",
            "price": 1600.00,
            "category": "dresses",
            "images": []
        }
        response = client.put("/products/1", json=product_data)
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_update_product_with_valid_data(self, client, auth_helper, test_db):
        """Test updating a product with valid data and authentication."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="admin2@example.com",
            password="adminpass123"
        )
        
        # Create a test product first
        test_product = Product(
            name="Original Product",
            description="Original Description",
            price=100.00,
            category="test",
            is_available=True
        )
        test_db.add(test_product)
        test_db.commit()
        test_db.refresh(test_product)
        
        # Update the product
        update_data = {
            "name": "Updated Product Name",
            "description": "Updated Description",
            "price": 150.00,
            "category": "updated_category",
            "images": ["image1.jpg", "image2.jpg"]
        }
        
        response = client.put(
            f"/products/{test_product.id}",
            json=update_data,
            headers=auth_helper.get_auth_headers("admin2@example.com")
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Product Name"
        assert data["description"] == "Updated Description"
        assert data["price"] == 150.00
        assert data["category"] == "updated_category"
        assert len(data["images"]) == 2
        assert data["is_available"] == True
    
    def test_update_nonexistent_product_returns_404(self, client, auth_helper):
        """Test that updating a non-existent product returns 404."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="admin3@example.com",
            password="adminpass123"
        )
        
        update_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 150.00,
            "category": "test",
            "images": []
        }
        
        response = client.put(
            "/products/99999",
            json=update_data,
            headers=auth_helper.get_auth_headers("admin3@example.com")
        )
        
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_delete_product_requires_authentication(self, client):
        """Test that DELETE /products/{id} requires authentication."""
        response = client.delete("/products/1")
        assert response.status_code == 401  # Changed from 403 to 401 for JWT
    
    def test_delete_product_with_valid_auth(self, client, auth_helper, test_db):
        """Test deleting a product with valid authentication (soft delete)."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="admin4@example.com",
            password="adminpass123"
        )
        
        # Create a test product first
        test_product = Product(
            name="Product To Delete",
            description="This will be deleted",
            price=100.00,
            category="test",
            is_available=True
        )
        test_db.add(test_product)
        test_db.commit()
        test_db.refresh(test_product)
        
        # Delete the product
        response = client.delete(
            f"/products/{test_product.id}",
            headers=auth_helper.get_auth_headers("admin4@example.com")
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_product.id
        assert data["is_available"] == False  # Should be soft-deleted
        
        # Verify the product still exists but is unavailable
        get_response = client.get(f"/products/{test_product.id}")
        assert get_response.status_code == 200
        product_data = get_response.json()
        assert product_data["is_available"] == False
    
    def test_delete_nonexistent_product_returns_404(self, client, auth_helper):
        """Test that deleting a non-existent product returns 404."""
        # Create authenticated user
        user_data, token = auth_helper.create_authenticated_user(
            email="admin5@example.com",
            password="adminpass123"
        )
        
        response = client.delete(
            "/products/99999",
            headers=auth_helper.get_auth_headers("admin5@example.com")
        )
        
        assert response.status_code == 404
        assert "detail" in response.json()
