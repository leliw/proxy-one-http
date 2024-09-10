"""Main file for FastAPI server"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.routers import config, proxy, storage
from app.static_files import static_file_response

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main_py")

openapi_tags = [
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
app.include_router(storage.router, prefix="/api/storage")


# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse, tags=["Angular files"])
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
