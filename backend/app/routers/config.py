from fastapi import APIRouter

from app.config import ClientConfig
from app.dependencies import ServerConfigDep


router = APIRouter(tags=["Konfiguracja klienta"])


@router.get("")
async def get_all(server_config: ServerConfigDep) -> ClientConfig:
    return ClientConfig(**server_config.model_dump())