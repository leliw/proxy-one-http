import pytest
import requests

from app.features.proxy.proxy_model import ProxySettings, ProxyStatus


@pytest.fixture
def settings(tmp_port):
    return ProxySettings(target_url="http://example.com", port=tmp_port)


def test_start_request_stop(client, settings, tmp_port):
    ret = client.post("/api/proxy/start", json=settings.model_dump())
    assert 200 == ret.status_code
    r = ProxyStatus(**ret.json())
    assert tmp_port == r.port

    response = requests.get(f"http://localhost:{tmp_port}")
    assert 200 == response.status_code
    assert "<title>Example Domain</title>" in response.text

    ret = client.post("/api/proxy/stop")
    assert 200 == ret.status_code


def test_start_request_logs_stop(client, settings, tmp_port):
    # Start proxy
    ret = client.post("/api/proxy/start", json=settings.model_dump())
    assert 200 == ret.status_code

    # Send request to proxy
    response = requests.get(f"http://localhost:{tmp_port}")
    assert 200 == response.status_code

    # View proxy log - reqest is visible
    with client.websocket_connect("/api/proxy/logs") as websocket:
        response = websocket.receive_text()
    assert "(GET) / => 200" == response

    # Stop proxy
    ret = client.post("/api/proxy/stop")
    assert 200 == ret.status_code
