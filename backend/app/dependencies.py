from typing import Annotated

from fastapi import Depends
from app.config import ServerConfig


def get_server_config() -> ServerConfig:
    return ServerConfig()


ServerConfigDep = Annotated[ServerConfig, Depends(get_server_config)]
