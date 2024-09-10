import pytest
import requests
from app.config import UserConfig
from app.features.proxy.proxy_server_manager import ProxyServerManager


@pytest.fixture
def server_manager(factory):
    sm = ProxyServerManager(factory)
    sm.start(UserConfig(target_url="http://example.com", port=8999))
    yield sm
    sm.stop()


def test_init(factory):
    t = ProxyServerManager(factory)

    assert t is not None


def test_start_status_stop(factory):
    t = ProxyServerManager(factory)

    assert t.start(UserConfig()) is not None
    s = t.get_status()
    assert s.status == "working"
    assert t.stop() is not None
    s = t.get_status()
    assert s.status == "stopped"


def test_get_request(server_manager):
    response = requests.get("http://localhost:8999")

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text


def test_post_request(server_manager):
    response = requests.post("http://localhost:8999", json={"test": "test"})

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text


# def test_put_request(server_manager):
#     response = requests.put("http://localhost:8999", json={"test": "test"})

#     assert 200 == response.status_code
#     assert "<title>Example Domain</title>" in response.text
