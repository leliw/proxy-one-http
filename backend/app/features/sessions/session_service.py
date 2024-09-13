from typing import List
from ampf.base.ampf_base_factory import AmpfBaseFactory
from app.features.sessions.session_model import Session, SessionRequest


class SessionService:
    def __init__(self, factory: AmpfBaseFactory) -> None:
        self._current_session: Session = None
        self._factory = factory
        self.storage = factory.create_storage("sessions", Session)

    # def get_all(self) -> List[Session]:
    #     return [Session(**i.model_dump(by_alias=True)) for i in self.storage.get_all()]

    def get_all(self) -> List[Session]:
        return self.storage.get_all()

    def get(self, key: str) -> Session:
        return self.storage.get(key)

    def start_session(self, target_url: str, description: str = None):
        """Starts session"""
        self._current_session = Session(target_url=target_url, description=description)

    def stop_session(self):
        """Stops current session"""
        self.storage.save(self._current_session)
        self._current_session = None

    def add(self, req: SessionRequest) -> None:
        """Adds request in current session"""
        self._current_session.requests_cnt += 1
        self.storage.save(self._current_session)
        self.save_req(req)

    def save_req(self, req: SessionRequest):
        """Saves request within session"""
        file_name = "_".join(
            [
                str(req.start).replace(" ", "_"),
                req.method,
                req.url.replace("/", "_"),
                str(req.status_code),
            ]
        )
        storage = self._factory.create_storage(
            f"sessions/{self._current_session.session_id}", SessionRequest
        )
        storage.put(file_name, req)
