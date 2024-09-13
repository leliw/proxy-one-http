import time
from datetime import datetime
import logging
import pytest
import requests
from ampf.base.base_storage import BaseStorage
from app.features.proxy.proxy_model import ProxySettings
from app.features.proxy.proxy_server_manager import ProxyServerManager
from app.features.sessions.session_model import SessionRequest
from app.features.sessions.session_service import SessionService


@pytest.fixture
def session_service(factory):
    logging.getLogger("ampf.local.json_multi_files_storage").setLevel(logging.DEBUG)
    return SessionService(factory)


@pytest.fixture
def server_manager(session_service, tmp_port):
    sm = ProxyServerManager(session_service)
    sm.start(ProxySettings(target_url="http://example.com", port=tmp_port))
    yield sm
    sm.stop()


@pytest.fixture
def storage(factory) -> BaseStorage[SessionRequest]:
    sub_path = "example.com/" + datetime.now().strftime("%Y-%m-%d")
    return factory.create_storage(
        f"sessions/{sub_path}", SessionRequest, key_name="file_name"
    )


def test_init(session_service):
    t = ProxyServerManager(session_service)

    assert t is not None


def test_start_status_stop(session_service, tmp_port):
    t = ProxyServerManager(session_service)

    assert t.start(ProxySettings(port=tmp_port, session_description="XXX")) is not None
    s = t.get_status()
    assert s.status == "working"
    assert t.stop() is not None
    s = t.get_status()
    assert s.status == "stopped"


def test_get_request(server_manager, session_service, tmp_port):
    logging.getLogger("ampf.local.json_multi_files_storage")
    response = requests.get(f"http://localhost:{tmp_port}")

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = list(session_service.get_all())
    assert 1 == len(keys)

    item = keys[0]
    assert "http://example.com" == item.target_url


def test_post_request(server_manager, session_service, tmp_port):
    response = requests.post(f"http://localhost:{tmp_port}", json={"test": "test"})

    assert 405 == response.status_code
    # assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = list(session_service.get_all())
    assert 1 == len(keys)
    item = keys[0]
    assert "http://example.com" == item.target_url


def test_put_request(server_manager, session_service, tmp_port):
    response = requests.put(f"http://localhost:{tmp_port}", json={"test": "test"})

    assert 405 == response.status_code
    # assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = list(session_service.get_all())
    assert 1 == len(keys)
    item = keys[0]
    assert "http://example.com" == item.target_url
