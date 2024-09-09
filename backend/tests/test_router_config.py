import os
from fastapi.testclient import TestClient
import pytest

from app.config import ServerConfig
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_server_config_default_values():
    config = ServerConfig()

    assert isinstance(config.version, str)


def test_client_config(client):
    result = client.get("/api/config")

    r = result.json()
    assert 200 == result.status_code
    assert "version" in r.keys()
