import logging
from typing import Iterator, List
from ampf.base.ampf_base_factory import BaseStorage
from app.features.sessions.session_model import SessionRequest, SessionRequestHeader, SessionRequestPatch


class SessionRequestService:
    def __init__(self, storage: BaseStorage[SessionRequest]) -> None:
        self.storage = storage
        self._log = logging.getLogger(__name__)

    def keys(self) -> Iterator[str]:
        for k in self.storage.keys():
            yield k

    def get_all(self) -> List[SessionRequestHeader]:
        return [
            SessionRequestHeader(**i.model_dump(by_alias=True))
            for i in self.storage.get_all()
        ]

    def post(self, req: SessionRequest) -> None:
        self.storage.create(req)

    def get(self, key: str) -> SessionRequest:
        return self.storage.get(key)

    def put(self, key: str, item: SessionRequest) -> None:
        self._log.debug("put %s", key)
        self.storage.put(key, item)

    def delete(self, key: str) -> bool:
        return self.storage.delete(key)

    def patch(self, key: str, patch_data: SessionRequestPatch) -> None:
        self._log.debug("patch %s", key)
        item = self.storage.get(key)
        patch_dict = patch_data.model_dump(exclude_unset=True)
        item.__dict__.update(patch_dict)
        self.storage.put(key, item)