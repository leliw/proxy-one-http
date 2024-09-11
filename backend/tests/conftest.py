import pytest

from ampf.local.ampf_local_factory import AmpfLocalFactory
from app.config import ServerConfig


@pytest.fixture
def server_config(tmp_path) -> ServerConfig:
    return ServerConfig(data_dir=str(tmp_path))


@pytest.fixture
def factory(tmp_path):
    return AmpfLocalFactory(tmp_path)
