import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="session")
def api_client():
    return TestClient(app)
