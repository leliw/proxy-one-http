from fastapi.testclient import TestClient
import pytest

from ampf.local.ampf_local_factory import AmpfLocalFactory
from  app.main import app
from app.config import ServerConfig
from app.dependencies import get_factory, get_server_config


@pytest.fixture
def server_config(tmp_path) -> ServerConfig:
    return ServerConfig(data_dir=str(tmp_path))


@pytest.fixture
def factory(tmp_path):
    return AmpfLocalFactory(tmp_path)

@pytest.fixture
def client(factory, server_config):
    app.dependency_overrides[get_factory] = lambda: factory
    app.dependency_overrides[get_server_config] = lambda: server_config
    return TestClient(app)