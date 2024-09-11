from typing import List
from ampf.base.ampf_base_factory import AmpfBaseFactory
from app.features.sessions.session_model import Session, SessionRequest


class SessionService:
    def __init__(self, factory: AmpfBaseFactory) -> None:
        self._factory = factory
        self.storage = factory.create_storage(
            "proxy", SessionRequest, key_name="file_name"
        )

    # def get_all(self) -> List[Session]:
    #     return [Session(**i.model_dump(by_alias=True)) for i in self.storage.get_all()]

    def get_all(self) -> List[str]:
        return list(self.storage.keys())

    def get(self, key: str) -> SessionRequest:
        return self.storage.get(key)

    def put(self, key: str, item: SessionRequest) -> None:
        self.storage.put(key, item)