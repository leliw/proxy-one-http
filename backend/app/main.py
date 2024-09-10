"""Main file for FastAPI server"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.routers import config, proxy
from app.static_files import static_file_response
from storage.directory_storage import DirectoryStorage
import app.model as model

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main_py")

storage = DirectoryStorage(base_path="data/proxy")


openapi_tags = [
    {
        "name": "Proxy",
        "description": "Proxy server",
    },
    {
        "name": "Storage",
        "description": "Stored requests",
    },
    {
        "name": "Angular files",
        "description": "Static Angular files",
    },
]

app = FastAPI(openapi_tags=openapi_tags)
app.include_router(config.router, prefix="/api/config")
app.include_router(proxy.router, prefix="/api/proxy")


@app.get("/api/storage", tags=["Storage"])
async def get_keys(path: str = None) -> list[str]:
    """Returns list of folders"""
    return storage.keys(sub_path=path)


@app.get("/api/storage/{key}", tags=["Storage"])
async def get_key(key: str, path: str = None) -> model.Request:
    """Returns file content"""
    return model.Request.parse_obj(storage.get(key=key, sub_path=path, file_ext="json"))


# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse, tags=["Angular files"])
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
