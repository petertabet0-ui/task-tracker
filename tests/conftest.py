import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import _reset


@pytest.fixture
def client():
    _reset()
    with TestClient(app) as test_client:
        yield test_client
    _reset()
