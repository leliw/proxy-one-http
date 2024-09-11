import pytest

from app.features.sessions.session_model import Session, SessionRequest
from app.features.sessions.session_service import SessionService


@pytest.fixture
def session_service(factory) -> SessionService:
    return SessionService(factory)


def test_get_empty(client):
    result = client.get("/api/sessions")

    assert 200 == result.status_code
    r = result.json()
    assert 0 == len(r)


def test_get_one(client, session_service):
    session_service.start_session(target_url="test")
    session_service.add(SessionRequest(url="/", method="GET"))
    session_service.stop_session()

    result = client.get("/api/sessions")

    assert 200 == result.status_code
    r = result.json()
    assert 1 == len(r)

    key = r[0]

    result = client.get(f"/api/sessions/{key}")

    assert 200 == result.status_code
    r = Session(**result.json())
    assert 1 == r.requests_cnt
