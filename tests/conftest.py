import pytest
from fastapi.testclient import TestClient

from fast_api_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)
