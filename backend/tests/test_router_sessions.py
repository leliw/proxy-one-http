import os
from fastapi.testclient import TestClient
import pytest

from app.config import ServerConfig
from app.dependencies import get_factory, get_server_config
from app.main import app


@pytest.fixture
def server_config(tmp_path) -> ServerConfig:
    os.makedirs(tmp_path.joinpath("proxy"), exist_ok=True)
    return ServerConfig(data_dir=str(tmp_path))


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
