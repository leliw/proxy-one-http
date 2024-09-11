import pytest
import requests
from app.features.proxy.proxy_model import ProxySettings

@pytest.fixture
def proxy(client, tmp_port):
    settings = ProxySettings(target_url="http://example.com", port=tmp_port).model_dump()
    result = client.post("/api/proxy/start", json=settings)
    assert 200 == result.status_code

    yield client

    result = client.post("/api/proxy/stop")
    assert 200 == result.status_code


def test_get_request_sessions(proxy, tmp_port):

    result = requests.get(f"http://localhost:{tmp_port}")
    assert 200 == result.status_code

    result = proxy.get("/api/sessions")
    assert 200 == result.status_code
    r = result.json()
    assert 1 == len(r)
