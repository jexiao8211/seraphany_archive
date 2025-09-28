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
        """Test that GET /products returns a list of products."""
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
        # Should return a list when no pagination parameters are used
        assert isinstance(data, list)
        assert len(data) == 2
    
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
        assert response.status_code == 403  # Forbidden (no token provided)
    
    def test_create_product_with_valid_data(self, client):
        """Test creating a product with valid data (when authenticated)."""
        # This test will be updated once we implement authentication
        product_data = {
            "name": "Vintage Chanel Dress",
            "description": "Beautiful vintage Chanel dress",
            "price": 1500.00,
            "category": "dresses",
            "images": ["image1.jpg", "image2.jpg"]
        }
        # For now, we'll expect 403 until auth is implemented
        response = client.post("/products", json=product_data)
        assert response.status_code == 403
    
    def test_update_product_requires_authentication(self, client):
        """Test that PUT /products/{id} requires authentication."""
        product_data = {
            "name": "Updated Vintage Chanel Dress",
            "price": 1600.00
        }
        response = client.put("/products/1", json=product_data)
        assert response.status_code == 403
    
    def test_delete_product_requires_authentication(self, client):
        """Test that DELETE /products/{id} requires authentication."""
        response = client.delete("/products/1")
        assert response.status_code == 403
