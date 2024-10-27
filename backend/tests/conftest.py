import logging
import random
from fastapi.testclient import TestClient
import pytest

from ampf.local.ampf_local_factory import AmpfLocalFactory
from app.features.sessions.session_model import Session, SessionReplay, SessionReplayRequest, SessionRequest
from app.features.sessions.session_service import SessionService
from app.main import app
from app.config import ServerConfig
from app.dependencies import get_factory, get_server_config


@pytest.fixture
def _log():
    log = logging.getLogger("test")
    log.setLevel(logging.DEBUG)
    return log

@pytest.fixture
def tmp_port():
    return random.randint(8000, 8998)


@pytest.fixture
def server_config(tmp_path, _log) -> ServerConfig:
    _log.info("fixture-server_config %s", tmp_path)
    return ServerConfig(data_dir=str(tmp_path))


@pytest.fixture
def factory(tmp_path):
    return AmpfLocalFactory(tmp_path)


@pytest.fixture
def client(factory, server_config):
    app.dependency_overrides[get_factory] = lambda: factory
    app.dependency_overrides[get_server_config] = lambda: server_config
    return TestClient(app)

@pytest.fixture
def session_storage(factory):
    storage = factory.create_storage("sessions", Session)
    repl_storage = factory.create_storage("replays", SessionReplay, "replay_id")
    repl_storage.add_subcollection(factory.create_storage("requests", SessionReplayRequest, "req_id"))
    storage.add_subcollection(repl_storage)
    storage.add_subcollection(factory.create_storage("requests", SessionRequest, "req_id"))
    return storage


@pytest.fixture
def session_service(session_storage) -> SessionService:
    return SessionService(session_storage)