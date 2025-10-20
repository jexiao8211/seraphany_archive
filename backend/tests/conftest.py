"""
Test configuration for SQLAlchemy tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app, get_database_service
from app.models import Base
from app.database import DatabaseService

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
def test_db_service(test_db):
    """Create a test database service with the test session"""
    # Create a custom database service that uses the test session
    class TestDatabaseService(DatabaseService):
        def get_session(self):
            return test_db
    
    return TestDatabaseService()

@pytest.fixture(scope="function")
def client(test_db, test_db_service):
    """Create a test client with overridden database dependency"""
    # Override the database dependency
    app.dependency_overrides[get_database_service] = lambda: test_db_service
    yield TestClient(app)
    # Clear overrides after test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_helper(client, test_db):
    """Create an authentication helper for tests"""
    from tests.auth_helpers import AuthTestHelper
    return AuthTestHelper(client, test_db)