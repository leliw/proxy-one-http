from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.dependencies import SessionStorageDep
from app.features.sessions.session_model import (
    SessionRequest,
    SessionRequestHeader,
    SessionRequestPatch,
)
from app.features.sessions.session_request_service import SessionRequestService


router = APIRouter(tags=["Żądania w sesji"])


def get_session_request_service(
    storage: SessionStorageDep, session_id: str
) -> SessionRequestService:
    return SessionRequestService(storage.get_collection(session_id, "requests"))


SessionRequestServiceDep = Annotated[
    SessionRequestService, Depends(get_session_request_service)
]


@router.get("")
async def get_all(service: SessionRequestServiceDep) -> List[SessionRequestHeader]:
    return service.get_all()


@router.get("/{req_id}")
async def get(service: SessionRequestServiceDep, req_id: str) -> SessionRequest:
    return service.get(req_id)


@router.patch("/{req_id}")
async def patch(
    service: SessionRequestServiceDep, req_id: str, data: SessionRequestPatch
) -> None:
    service.patch(req_id, data)
