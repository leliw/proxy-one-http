from fastapi.testclient import TestClient
import pytest

from app.dependencies import get_factory, get_server_config
from app.main import app


@pytest.fixture
def client(factory, server_config):
    app.dependency_overrides[get_factory] = lambda: factory
    app.dependency_overrides[get_server_config] = lambda: server_config
    return TestClient(app)


def test_get_empty(client):
    result = client.get("/api/sessions")

    r = result.json()
    assert 200 == result.status_code
    assert 0 == len(r)
