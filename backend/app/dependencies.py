from typing import Annotated

from fastapi import Depends
from ampf.base.ampf_base_factory import AmpfBaseFactory
from ampf.local.ampf_local_factory import AmpfLocalFactory
from app.config import ServerConfig


def get_server_config() -> ServerConfig:
    return ServerConfig()


ServerConfigDep = Annotated[ServerConfig, Depends(get_server_config)]


def get_factory(config: ServerConfigDep) -> AmpfBaseFactory:
    return AmpfLocalFactory(config.data_dir)


FactoryDep = Annotated[AmpfBaseFactory, Depends(get_factory)]
