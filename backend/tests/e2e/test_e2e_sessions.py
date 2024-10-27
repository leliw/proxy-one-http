import pytest
import requests
from app.features.proxy.proxy_model import ProxySettings, ProxyStatus
from app.features.sessions.session_model import SessionRequest, SessionRequestHeader


@pytest.fixture
def proxy(client, tmp_port):
    settings = ProxySettings(
        target_url="http://example.com", port=tmp_port, session_description="XXX"
    ).model_dump()
    result = client.post("/api/proxy/start", json=settings)
    assert 200 == result.status_code

    yield client
    status = ProxyStatus(**client.get("/api/proxy/status").json())
    if status.status == "working":
        result = client.post("/api/proxy/stop")
        assert 200 == result.status_code


def test_get_request_sessions(proxy, tmp_port):
    result = requests.get(f"http://localhost:{tmp_port}")
    assert 200 == result.status_code

    result = proxy.get("/api/sessions")
    assert 200 == result.status_code
    r = result.json()
    assert 1 == len(r)
    assert "XXX" == r[0]["description"]

    session_id = r[0]["session_id"]
    result = proxy.get(f"/api/sessions/{session_id}/requests")

    assert 200 == result.status_code
    r = result.json()
    item = SessionRequestHeader(**r[0])
    assert "text/html; charset=UTF-8" == item.resp_content_type
    assert 1256 == item.resp_content_length

    req_id = r[0]["req_id"]
    result = proxy.get(f"/api/sessions/{session_id}/requests/{req_id}")
    assert 200 == result.status_code
    r = SessionRequest(**result.json())
    assert "GET" == r.method


def test_delete_session(proxy, tmp_port):
    requests.get(f"http://localhost:{tmp_port}")
    result = proxy.get("/api/sessions")
    assert 200 == result.status_code
    r = result.json()
    assert 1 == len(r)
    session_id = r[0]["session_id"]

    result = proxy.delete(f"/api/sessions/{session_id}")

    assert 200 == result.status_code
    result = proxy.get("/api/sessions")
    assert 200 == result.status_code
    r = result.json()
    assert 0 == len(r)
