"""
Tests for product-related API endpoints.
Following TDD approach - tests written before implementation.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestProductEndpoints:
    """Test cases for product API endpoints."""
    
    def test_get_products_returns_list(self):
        """Test that GET /products returns a list of products."""
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        # Should return a list when no pagination parameters are used
        assert isinstance(data, list)
    
    def test_get_products_with_pagination(self):
        """Test that GET /products supports pagination."""
        response = client.get("/products?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
    
    def test_get_products_with_category_filter(self):
        """Test that GET /products filters by category."""
        response = client.get("/products?category=dresses")
        assert response.status_code == 200
        # In a real test, we'd verify all returned products have category="dresses"
    
    def test_get_products_with_search(self):
        """Test that GET /products supports search functionality."""
        response = client.get("/products?search=vintage")
        assert response.status_code == 200
        # In a real test, we'd verify search results contain "vintage"
    
    def test_get_single_product(self):
        """Test that GET /products/{id} returns a single product."""
        # This test will fail initially since we haven't implemented the endpoint
        response = client.get("/products/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "price" in data
        assert "description" in data
    
    def test_get_nonexistent_product_returns_404(self):
        """Test that GET /products/{id} returns 404 for non-existent product."""
        response = client.get("/products/99999")
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_create_product_requires_authentication(self):
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
    
    def test_create_product_with_valid_data(self):
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
    
    def test_update_product_requires_authentication(self):
        """Test that PUT /products/{id} requires authentication."""
        product_data = {
            "name": "Updated Vintage Chanel Dress",
            "price": 1600.00
        }
        response = client.put("/products/1", json=product_data)
        assert response.status_code == 403
    
    def test_delete_product_requires_authentication(self):
        """Test that DELETE /products/{id} requires authentication."""
        response = client.delete("/products/1")
        assert response.status_code == 403
