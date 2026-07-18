"""Shared pytest fixtures for the Smart Stadium AI System test suite."""
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["DATABASE_URL"] = "sqlite:///./test_smart_stadium.db"
os.environ["ADMIN_API_KEY"] = "test-admin-key"

from fastapi.testclient import TestClient  # noqa: E402
from app.database.base import Base  # noqa: E402
from app.database.session import get_db  # noqa: E402
import app.models  # noqa: E402,F401
from app.main import app  # noqa: E402

TEST_DATABASE_URL = "sqlite:///./test_smart_stadium.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a clean database session for each test function."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Provide a TestClient wired to the isolated test database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers():
    """Return the admin authentication header for protected endpoints."""
    return {"X-Admin-Key": "test-admin-key"}
