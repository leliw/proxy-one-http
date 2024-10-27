import json
from typing import Generator
from fastapi.testclient import TestClient
import pytest
import requests
from app.features.proxy.proxy_model import ProxySettings, ProxyStatus


@pytest.fixture
def proxy(client, tmp_port) -> Generator[TestClient, None, None]:
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


def test_record_and_replay(proxy, tmp_port):
    # Record request
    result = requests.get(f"http://localhost:{tmp_port}")
    assert 200 == result.status_code
    result = requests.get(f"http://localhost:{tmp_port}/?q=hello!")
    assert 200 == result.status_code


    # Stop recording session
    result = proxy.post("/api/proxy/stop")
    assert 200 == result.status_code

    # Get session_id
    result = proxy.get("/api/sessions")
    assert 200 == result.status_code
    r = result.json()
    session_id = r[0]["session_id"]

    # Enable all requests
    result = proxy.get(f"/api/sessions/{session_id}/requests")
    assert 200 == result.status_code
    r = json.loads(result.text)
    for req in r:
        result = proxy.patch(f"/api/sessions/{session_id}/requests/{req['req_id']}", json={"disabled":False})
        assert 200 == result.status_code

    # Replay session
    result = proxy.post(f"/api/sessions/{session_id}/replays")
    assert 200 == result.status_code
    r = json.loads(f"[{result.text}]")

    assert "/" == r[0]["url"]
    assert "/?q=hello!" == r[1]["url"]
