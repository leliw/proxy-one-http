import pytest

from app.features.sessions.session_model import SessionRequest
from app.features.sessions.session_service import SessionService


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
