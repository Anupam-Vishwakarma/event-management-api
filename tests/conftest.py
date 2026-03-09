"""
Pytest configuration and shared fixtures for Event Management API tests.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

from app.main import app
from app.database import Base, get_db
from app import models


# Create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine with in-memory SQLite."""
    from sqlalchemy.pool import StaticPool
    
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_event_data():
    """Sample event data for testing."""
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    return {
        "title": "Python Conference 2026",
        "description": "Annual Python conference with workshops",
        "location": "San Francisco, CA",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "max_capacity": 100
    }


@pytest.fixture
def sample_participant_data():
    """Sample participant data for testing."""
    return {
        "name": "John Doe",
        "email": "john@example.com"
    }


@pytest.fixture
def sample_participant_data_2():
    """Second sample participant for testing duplicates."""
    return {
        "name": "Jane Smith",
        "email": "jane@example.com"
    }


@pytest.fixture
def sample_participant_data_invalid_email():
    """Sample participant with invalid email."""
    return {
        "name": "Invalid User",
        "email": "not-an-email"
    }


@pytest.fixture
def created_event(client, sample_event_data):
    """Create a sample event and return the response."""
    response = client.post("/events/", json=sample_event_data)
    return response.json()


@pytest.fixture
def created_event_small_capacity(client):
    """Create an event with small capacity for testing."""
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    event_data = {
        "title": "Small Event",
        "description": "Small capacity event",
        "location": "NYC",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "max_capacity": 1
    }
    response = client.post("/events/", json=event_data)
    return response.json()
