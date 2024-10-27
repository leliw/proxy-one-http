import logging
from typing import Iterator, List
from ampf.base import BaseCollectionStorage
from .session_model import Session, SessionRequest
from .session_request_service import SessionRequestService


class SessionService:
    def __init__(self, storage: BaseCollectionStorage[Session]) -> None:
        self._current_session: Session = None
        self.storage = storage
        self._log = logging.getLogger(__name__)

    # def get_all(self) -> List[Session]:
    #     return [Session(**i.model_dump(by_alias=True)) for i in self.storage.get_all()]

    def get_all(self) -> List[Session]:
        return self.storage.get_all()

    def get(self, key: str) -> Session:
        return self.storage.get(key)

    def put(self, key: str, session: Session) -> None:
        return self.storage.put(key, session)

    def delete(self, key: str) -> None:
        return self.storage.delete(key)

    def create_request_service(self, session_id: str = None) -> SessionRequestService:
        return SessionRequestService(
            self.storage.get_collection(session_id or self._current_session.session_id, "requests")
        )

    def start_session(self, target_url: str, description: str = None):
        """Starts session"""
        self._current_session = Session(target_url=target_url, description=description)

    def stop_session(self):
        """Stops current session"""
        self.storage.save(self._current_session)
        self._current_session = None

    def add_session_request(self, req: SessionRequest) -> None:
        """Adds request in current session"""
        self._current_session.requests_cnt += 1
        self._current_session.req_ids.append(req.req_id)
        self.storage.save(self._current_session)
        self.create_request_service().post(req)

    def get_requests(self, session_id: str) -> Iterator[SessionRequest]:
        """Returns all session request in oryginal order"""
        session = self.get(session_id)
        service = self.create_request_service(session_id)
        for req_id in session.req_ids:
            yield service.get(req_id)
