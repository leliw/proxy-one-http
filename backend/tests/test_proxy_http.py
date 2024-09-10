import time
from datetime import datetime
import logging
import pytest
import requests
from ampf.base.base_storage import BaseStorage
from app import model
from app.config import UserConfig
from app.features.proxy.proxy_server_manager import ProxyServerManager


@pytest.fixture
def server_manager(factory):
    sm = ProxyServerManager(factory)
    sm.start(UserConfig(target_url="http://example.com", port=8999))
    yield sm
    sm.stop()

@pytest.fixture
def storage(factory) -> BaseStorage[model.Request]:
    logging.getLogger("ampf.local.json_multi_files_storage").setLevel(logging.DEBUG)
    sub_path = "example.com/" + datetime.now().strftime("%Y-%m-%d")
    return factory.create_storage(f"sessions/{sub_path}", model.Request, key_name="file_name")

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


def test_get_request(server_manager, storage):
    response = requests.get("http://localhost:8999")

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = list(storage.keys())
    assert 1 == len(keys)
    assert "GET" in keys[0]
    item = storage.get(keys[0])
    assert "GET" == item.method



def test_post_request(server_manager, storage):
    response = requests.post("http://localhost:8999", json={"test": "test"})

    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text

    time.sleep(0.1)
    keys = list(storage.keys())
    assert 1 == len(keys)
    assert "POST" in keys[0]
    item = storage.get(keys[0])
    assert "POST" == item.method



# def test_put_request(server_manager):
#     response = requests.put("http://localhost:8999", json={"test": "test"})

#     assert 200 == response.status_code
#     assert "<title>Example Domain</title>" in response.text
