import time
from datetime import datetime
import logging
import pytest
import requests
from ampf.base.base_storage import BaseStorage
from app.config import UserConfig
from app.features.proxy.proxy_server_manager import ProxyServerManager
from app.features.sessions.session_model import SessionRequest
from app.features.sessions.session_service import SessionService


@pytest.fixture
def session_service(factory):
    logging.getLogger("ampf.local.json_multi_files_storage").setLevel(logging.DEBUG)
    return SessionService(factory)

@pytest.fixture
def server_manager(session_service):
    sm = ProxyServerManager(session_service)
    sm.start(UserConfig(target_url="http://example.com", port=8999))
    yield sm
    sm.stop()

@pytest.fixture
def storage(factory) -> BaseStorage[SessionRequest]:
    sub_path = "example.com/" + datetime.now().strftime("%Y-%m-%d")
    return factory.create_storage(f"sessions/{sub_path}", SessionRequest, key_name="file_name")

def test_init(session_service):
    t = ProxyServerManager(session_service)

    assert t is not None


def test_start_status_stop(session_service):
    t = ProxyServerManager(session_service)

    assert t.start(UserConfig()) is not None
    s = t.get_status()
    assert s.status == "working"
    assert t.stop() is not None
    s = t.get_status()
    assert s.status == "stopped"


def test_get_request(server_manager, session_service):
    response = requests.get("http://localhost:8999")

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = session_service.get_all()
    assert 1 == len(keys)
    assert "GET" in keys[0]
    item = session_service.get(keys[0])
    assert "GET" == item.method



def test_post_request(server_manager, session_service):
    response = requests.post("http://localhost:8999", json={"test": "test"})

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = session_service.get_all()
    assert 1 == len(keys)
    assert "POST" in keys[0]
    item = session_service.get(keys[0])
    assert "POST" == item.method



# def test_put_request(server_manager):
#     response = requests.put("http://localhost:8999", json={"test": "test"})

#     assert 200 == response.status_code
#     assert "<title>Example Domain</title>" in response.text
