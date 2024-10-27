import logging
from typing import Iterator, List

from ampf.base import BaseCollectionStorage
from app.features.sessions.session_model import (
    SessionReplay,
    SessionReplayHeader,
    SessionReplayRequest,
    SessionRequest,
    SessionRequestHeader,
)
from app.features.sessions.session_replayer import SessionReplayer
from app.features.sessions.session_service import SessionService


class SessionReplayService:
    def __init__(
        self,
        storage: BaseCollectionStorage[SessionReplay],
        session_service: SessionService,
    ) -> None:
        self.storage = storage
        self.session_service = session_service
        self._current_replay: SessionReplay = None
        self._log = logging.getLogger(__name__)

    def keys(self) -> Iterator[str]:
        for k in self.storage.keys():
            yield k

    def get_all(self) -> List[SessionReplayHeader]:
        return [
            SessionReplayHeader(**i.model_dump(by_alias=True))
            for i in self.storage.get_all()
        ]

    def post(self, replay: SessionReplay) -> None:
        self.storage.create(replay)

    def get(self, key: str) -> SessionRequest:
        return self.storage.get(key)

    def put(self, key: str, item: SessionRequest) -> None:
        self._log.debug("put %s", key)
        self.storage.put(key, item)

    def delete(self, key: str) -> bool:
        return self.storage.delete(key)

    def replay(self, session_id: str) -> Iterator[SessionRequestHeader]:
        self._current_replay = SessionReplay(session_id=session_id)
        self.post(self._current_replay)
        replayer = SessionReplayer(
            self.session_service.get(session_id),
            self.session_service.get_requests(session_id),
        )
        for req in replayer.replay():
            self.add_request(req)
            yield SessionRequestHeader(**req.model_dump(exclude_none=True))
        self._current_replay = None

    def add_request(self, req: SessionReplayRequest) -> None:
        """Adds request in current session"""
        self._current_replay.requests_cnt += 1
        self._current_replay.req_ids.append(req.req_id)
        self.storage.save(self._current_replay)
        req_storage = self.storage.get_collection(
            self._current_replay.replay_id, "requests"
        )
        req_storage.save(req)
