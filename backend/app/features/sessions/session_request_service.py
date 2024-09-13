import logging
from typing import List, Optional
from ampf.base.ampf_base_factory import AmpfBaseFactory
from app.features.sessions.session_model import SessionRequest, SessionRequestHeader


class SessionRequestService:
    def __init__(self, factory: AmpfBaseFactory, session_id: str) -> None:
        self.storage = factory.create_storage(f"sessions/{session_id}", SessionRequest)
        self._log = logging.getLogger(__name__)
        
    def get_all(self) -> List[SessionRequestHeader]:
        return [
            SessionRequestHeader(**i.model_dump(by_alias=True))
            for i in self.storage.get_all()
        ]

    def post(self, req: SessionRequest) -> None:
        key = "_".join(
            [
                str(req.start).replace(" ", "_"),
                req.method,
                req.url.replace("/", "_"),
                str(req.status_code),
            ]
        )
        self.put(key, req)

    def get(self, key: str) -> Optional[SessionRequest]:
        return self.storage.get(key)

    def put(self, key: str, item: SessionRequest) -> None:
        self._log.debug("put %s", key)
        self.storage.put(key, item)

    def delete(self, key: str) -> bool:
        return self.storage.delete(key)
