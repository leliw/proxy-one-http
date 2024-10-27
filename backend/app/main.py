"""Main file for FastAPI server"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.logging_config import setup_logging
from app.routers import (
    config,
    proxy,
    sessions,
    sessions_replays,
    sessions_replays_requests,
    sessions_requests,
)

setup_logging()

# fmt: off
app = FastAPI()
app.include_router(prefix="/api/config",                                                router=config.router)
app.include_router(prefix="/api/proxy",                                                 router=proxy.router)
app.include_router(prefix="/api/sessions",                                              router=sessions.router)
app.include_router(prefix="/api/sessions/{session_id}/requests",                        router=sessions_requests.router)
app.include_router(prefix="/api/sessions/{session_id}/replays",                         router=sessions_replays.router)
app.include_router(prefix="/api/sessions/{session_id}/replays/{replay_id}/requests",    router=sessions_replays_requests.router)

app.mount("/", StaticFiles(directory="static/browser", html=True), name="static")
# fmt: on
