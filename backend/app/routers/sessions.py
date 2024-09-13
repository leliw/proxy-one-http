from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.dependencies import FactoryDep
from app.features.sessions.session_model import Session, SessionRequestHeader
from app.features.sessions.session_service import SessionService


router = APIRouter(tags=["Sessions"])


def get_service(factory: FactoryDep) -> SessionService:
    return SessionService(factory)


SessionServiceDep = Annotated[SessionService, Depends(get_service)]


@router.get("")
async def get_all(service: SessionServiceDep) -> List[Session]:
    """Returns list of folders"""
    return service.get_all()


@router.get("/{key}")
async def get(service: SessionServiceDep, key: str) -> Session:
    """Returns file content"""
    return service.get(key)

@router.get("/{key}/requests")
async def get_requests(service: SessionServiceDep, key: str) -> List[SessionRequestHeader]:
    req_service = service.create_request_service(key)
    return req_service.get_all()
