

import pytest

from app.features.sessions.session_model import SessionRequest, SessionRequestPatch
from app.features.sessions.session_request_service import SessionRequestService


@pytest.fixture
def session_request_service(session_service, session_storage) -> SessionRequestService:
    session_service.start_session(target_url="test")
    session_service.add_session_request(SessionRequest(url="/", method="GET"))
    session_service.stop_session()
    sessions = session_service.get_all()
    session_id = next(sessions).session_id
    return SessionRequestService(session_storage.get_collection(session_id, "requests"))

def test_patch_request(session_request_service):
    """Test disabling request by patch method"""
    ret = session_request_service.get_all()
    req_id = ret[0].req_id
    ret = session_request_service.patch(req_id, SessionRequestPatch(disabled=True))
    
    ret = session_request_service.get(req_id)

    assert ret.disabled