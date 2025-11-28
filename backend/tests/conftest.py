"""
Test configuration for SQLAlchemy tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database_config import get_db
from app.models import Base

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a test session
    session = TestingSessionLocal()
    
    yield session
    
    # Clean up
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database dependency"""
    # Override the database dependency
    def override_get_db():
        try:
            yield test_db
        finally:
            pass # Session closed by test_db fixture
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Clear overrides after test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_helper(client, test_db):
    """Create an authentication helper for tests"""
    from tests.auth_helpers import AuthTestHelper
    return AuthTestHelper(client, test_db)
