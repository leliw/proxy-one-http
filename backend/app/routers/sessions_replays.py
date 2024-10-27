from typing import Annotated, Iterator, List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.dependencies import SessionStorageDep
from app.features.sessions.session_model import SessionReplayHeader
from app.features.sessions.session_replay_service import SessionReplayService
from app.routers.sessions import SessionServiceDep

router = APIRouter(tags=["Odtworzenia sesji"])


def get_session_replay_service(
    session_storage: SessionStorageDep,
    session_service: SessionServiceDep,
    session_id: str,
) -> SessionReplayService:
    return SessionReplayService(
        session_storage.get_collection(session_id, "replays"), session_service
    )
    # return service.create_request_service(session_id)


SessionReplayServiceDep = Annotated[
    SessionReplayService, Depends(get_session_replay_service)
]


def json_to_text[T: BaseModel](responses: Iterator[T]) -> Iterator[str]:
    for i, r in enumerate(responses):
        yield f"{',' if i > 0 else ''}{r.model_dump_json()}\n"


@router.post("", responses={200: {"content": {"text/event-stream": {}}}})
def replay_session(service: SessionReplayServiceDep, session_id: str):
    responses = service.replay(session_id)
    return StreamingResponse(
        json_to_text(responses),
        media_type="text/event-stream",
    )


@router.get("")
def get_all(service: SessionReplayServiceDep) -> List[SessionReplayHeader]:
    """Returns list of folders"""
    return service.get_all()
