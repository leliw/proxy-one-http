from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.dependencies import SessionStorageDep
from app.features.sessions.session_model import (
    SessionReplayRequestDto,
    SessionReplayRequestHeader,
)
from app.features.sessions.session_replay_request_service import (
    SessionReplayRequestService,
)


router = APIRouter(tags=["Żądania w odtworzeniu sesji"])


def get_session_replay_request_service(
    session_storage: SessionStorageDep, session_id: str, replay_id: str
) -> SessionReplayRequestService:
    return SessionReplayRequestService(
        session_storage
            .get_collection(session_id, "requests"),
        session_storage
            .get_collection(session_id, "replays")
                .get_collection(replay_id, "requests")
    )  # fmt: skip


SessionReplayRequestServiceDep = Annotated[
    SessionReplayRequestService, Depends(get_session_replay_request_service)
]


@router.get("")
def get_all(
    service: SessionReplayRequestServiceDep,
) -> List[SessionReplayRequestHeader]:
    return service.get_all()


@router.get("/{req_id}")
def get(
    service: SessionReplayRequestServiceDep, req_id: str
) -> SessionReplayRequestDto:
    return service.get(req_id)
