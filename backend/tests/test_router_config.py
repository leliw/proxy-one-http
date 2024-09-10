from fastapi.testclient import TestClient
import pytest

from ampf.local.ampf_local_factory import AmpfLocalFactory
from app.config import ServerConfig
from app.dependencies import get_factory
from app.main import app

@pytest.fixture
def factory(tmp_path):
    return AmpfLocalFactory(tmp_path)

@pytest.fixture
def client(factory):
    app.dependency_overrides[get_factory] = lambda: factory
    return TestClient(app)


def test_server_config_default_values():
    config = ServerConfig()

    assert isinstance(config.version, str)


def test_client_config(client):
    result = client.get("/api/config")

    r = result.json()
    assert 200 == result.status_code
    assert "version" in r.keys()


def test_user_config_default(client):
    result = client.get("/api/config/user")

    r = result.json()
    assert 200 == result.status_code
    assert r["target_url"] == "http://example.com"

def test_user_config_put_get(client):
    result = client.put("/api/config/user", json={"target_url": "http://example.com.pl", "port": 8999})
    
    assert 200 == result.status_code

    result = client.get("/api/config/user")

    r = result.json()
    assert 200 == result.status_code
    assert r["target_url"] == "http://example.com.pl"