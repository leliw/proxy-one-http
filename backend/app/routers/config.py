from typing import Annotated
from fastapi import APIRouter, Depends

from app.config import ClientConfig, UserConfig, UserConfigService
from app.dependencies import FactoryDep, ServerConfigDep


router = APIRouter(tags=["Konfiguracja klienta i użytkownika"])


def get_service(factory: FactoryDep) -> UserConfigService:
    return UserConfigService(factory)


ServiceDep = Annotated[UserConfigService, Depends(get_service)]


@router.get("")
async def get_client_config(server_config: ServerConfigDep) -> ClientConfig:
    return ClientConfig(**server_config.model_dump())


@router.get("/user")
async def get_user_config(service: ServiceDep) -> UserConfig:
    return service.get() or UserConfig()


@router.put("/user")
async def put_user_config(service: ServiceDep, config: UserConfig):
    return service.put(config)
