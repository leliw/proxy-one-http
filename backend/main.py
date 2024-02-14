"""Main file for FastAPI server"""
import logging
import threading
from typing import Union
from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import HTMLResponse
from pyaml_env import parse_config
import proxy_http

from static_files import static_file_response

config = parse_config('./config.yaml')

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main_py")

server_manager = proxy_http.ServerManager()
server_manager.run()

openapi_tags = [
    {
        "name": "config",
        "description": "Config from yaml file",
    },
    {
        "name": "proxy",
        "description": "Proxy server",
    },
    {
        "name": "angular_files",
        "description": "Serves static Angular files",
    }
]

app = FastAPI(openapi_tags=openapi_tags)

@app.get("/api/config", tags=["config"])
async def read_config():
    """Return config from yaml file"""
    return config

@app.get("/api/start", tags=["proxy"])
async def proxy_start():
    """Starts the proxy server"""
    server_manager.stop()
    server_manager.run()
    return {"status": "Server started"}

@app.get("/api/status", tags=["proxy"])
async def proxy_status() -> proxy_http.Status:
    """Return porxy server status"""
    return server_manager.get_status()

# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse, tags=["angular_files"])
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
