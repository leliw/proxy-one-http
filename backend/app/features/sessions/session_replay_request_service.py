import logging
from typing import List

from ampf.base.base_collection_storage import BaseCollectionStorage
from app.features.sessions.session_model import (
    SessionReplayRequest,
    SessionReplayRequestDto,
    SessionReplayRequestHeader,
    SessionRequest,
)


class SessionReplayRequestService:
    def __init__(
        self,
        org_storage: BaseCollectionStorage[SessionRequest],
        repl_storage: BaseCollectionStorage[SessionReplayRequest],
    ) -> None:
        self.org_storage = org_storage
        self.repl_storage = repl_storage
        self._log = logging.getLogger(__name__)

    def get_all(self) -> List[SessionReplayRequestHeader]:
        return [
            SessionReplayRequestHeader(**d.model_dump())
            for d in self.repl_storage.get_all()
        ]

    def get(self, key: str) -> SessionReplayRequestDto:
        """Returns oryginal and replayed request."""
        org = self.org_storage.get(key)
        repl = self.repl_storage.get(key)
        return SessionReplayRequestDto.create(org, repl)
