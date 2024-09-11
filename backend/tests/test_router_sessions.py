from fastapi.testclient import TestClient
import pytest

from app.dependencies import get_factory, get_server_config
from app.features.sessions.session_model import SessionRequest
from app.features.sessions.session_service import SessionService
from app.main import app


@pytest.fixture
def client(factory, server_config):
    app.dependency_overrides[get_factory] = lambda: factory
    app.dependency_overrides[get_server_config] = lambda: server_config
    return TestClient(app)

@pytest.fixture
def session_service(factory):
    return SessionService(factory) 

def test_get_empty(client):
    result = client.get("/api/sessions")

    assert 200 == result.status_code
    r = result.json()
    assert 0 == len(r)

def test_get_one(client, session_service):
    session_service.put("test", SessionRequest(url="/", method="GET"))

    result = client.get("/api/sessions")

    assert 200 == result.status_code
    r = result.json()
    assert 1 == len(r)
    
    key = r[0]

    result = client.get(f"/api/sessions/{key}")
    
    assert 200 == result.status_code
    r = SessionRequest(**result.json())
    assert "/" == r.url
    assert "GET" == r.method
