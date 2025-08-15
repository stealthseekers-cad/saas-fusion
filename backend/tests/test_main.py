import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

# --- Test Database Setup ---
# Use an in-memory SQLite database for testing. It's fast and isolated.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create the tables in the test database before tests run
Base.metadata.create_all(bind=engine)


# --- Dependency Override ---
# This function will replace the real `get_db` function during tests.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Tell the app to use our new fake database function for all tests
app.dependency_overrides[get_db] = override_get_db

# Create a test client for our FastAPI app
client = TestClient(app)


# --- Tests ---
def test_read_root():
    """
    Test that the root endpoint ("/") is reachable and returns a
    successful (200 OK) response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Hello": "Stealth Seekers Foresight Engine is Online"
    }
