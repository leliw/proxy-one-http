from typing import Annotated
from fastapi import APIRouter, Depends

from app.dependencies import FactoryDep
from app.features.sessions.session_model import Session
from app.features.sessions.session_service import SessionService


router = APIRouter(tags=["Sessions"])


def get_service(factory: FactoryDep) -> SessionService:
    return SessionService(factory)


SessionServiceDep = Annotated[SessionService, Depends(get_service)]


@router.get("")
async def get_all(service: SessionServiceDep) -> list[Session]:
    """Returns list of folders"""
    return service.get_all()


@router.get("/{key}")
async def get(service: SessionServiceDep, key: str) -> Session:
    """Returns file content"""
    return service.get(key)
