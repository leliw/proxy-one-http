"""Main file for FastAPI server"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import config, proxy, sessions


app = FastAPI()
app.include_router(config.router, prefix="/api/config")
app.include_router(proxy.router, prefix="/api/proxy")
app.include_router(sessions.router, prefix="/api/sessions")

app.mount("/", StaticFiles(directory="static/browser", html=True), name="static")
