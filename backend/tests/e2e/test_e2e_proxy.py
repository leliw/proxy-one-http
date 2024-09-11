import pytest
from app.features.proxy.proxy_model import ProxySettings, ProxyStatus

@pytest.fixture
def proxy_settings_example(tmp_port) -> dict:
    return ProxySettings(target_url="http://example.com", port=tmp_port).model_dump()

def test_start_status_stop(client, proxy_settings_example):
    result = client.post("/api/proxy/start", json=proxy_settings_example)
    assert 200 == result.status_code

    result = client.get("/api/proxy/status")
    assert 200 == result.status_code
    r = ProxyStatus(**result.json())
    assert "working" == r.status

    result = client.post("/api/proxy/stop")
    assert 200 == result.status_code

    result = client.get("/api/proxy/status")
    assert 200 == result.status_code
    r = ProxyStatus(**result.json())
    assert "stopped" == r.status

def test_get_request(client, proxy_settings_example):
    pass