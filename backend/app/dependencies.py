from typing import Annotated

from fastapi import Depends

from ampf.base import AmpfBaseFactory, BaseCollectionStorage, CollectionDef
from ampf.local import AmpfLocalFactory
from app.config import ServerConfig
from app.features.sessions.session_model import (
    Session,
    SessionReplay,
    SessionReplayRequest,
    SessionRequest,
)


def get_server_config() -> ServerConfig:
    return ServerConfig()


ServerConfigDep = Annotated[ServerConfig, Depends(get_server_config)]


def get_factory(config: ServerConfigDep) -> AmpfBaseFactory:
    return AmpfLocalFactory(config.data_dir)


FactoryDep = Annotated[AmpfBaseFactory, Depends(get_factory)]


def get_session_storage(factory: FactoryDep):
    return factory.create_collection(
        CollectionDef(collection_name="sessions", clazz=Session, key_name="session_id", subcollections=[
                CollectionDef(collection_name="requests", clazz=SessionRequest, key_name="req_id"),
                CollectionDef(collection_name="replays", clazz=SessionReplay, key_name="replay_id", subcollections=[
                        CollectionDef(collection_name="requests", clazz=SessionReplayRequest, key_name="req_id")
                    ]
                )
            ]
        )
    )  # fmt: skip


SessionStorageDep = Annotated[
    BaseCollectionStorage[Session], Depends(get_session_storage)
]
