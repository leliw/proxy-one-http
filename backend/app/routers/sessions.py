from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.dependencies import SessionStorageDep
from app.features.sessions.session_model import Session
from app.features.sessions.session_service import SessionService


router = APIRouter(tags=["Sesje"])


def get_service(storage: SessionStorageDep) -> SessionService:
    return SessionService(storage)


SessionServiceDep = Annotated[SessionService, Depends(get_service)]


@router.get("")
def get_all(service: SessionServiceDep) -> List[Session]:
    """Returns list of folders"""
    return service.get_all()


@router.get("/{session_id}")
async def get(service: SessionServiceDep, session_id: str) -> Session:
    """Returns file content"""
    return service.get(session_id)


@router.put("/{session_id}")
async def put(service: SessionServiceDep, session_id: str, session: Session) -> None:
    service.put(session_id, session)


@router.delete("/{session_id}")
async def delete(service: SessionServiceDep, session_id: str) -> None:
    service.delete(session_id)
