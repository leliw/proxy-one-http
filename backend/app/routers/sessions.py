from typing import Annotated
from fastapi import APIRouter, Depends

from ampf.base.base_storage import BaseStorage
from app.dependencies import FactoryDep
from app.features.sessions import session_model


router = APIRouter(tags=["Sessions storage"])


def get_service(factory: FactoryDep):
    return factory.create_storage("proxy", session_model.Request, key_name="file_name")


ServiceDep = Annotated[BaseStorage, Depends(get_service)]


@router.get("")
async def get_keys(service: ServiceDep) -> list[str]:
    """Returns list of folders"""
    return service.keys()


@router.get("/{key}")
async def get_key(service: ServiceDep, key: str) -> session_model.Request:
    """Returns file content"""
    return service.get(key)
