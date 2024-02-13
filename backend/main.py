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
log.setLevel(logging.INFO)

log.info("Starting proxy server ...")
server_manager = proxy_http.ServerManager()
server_manager.run()
log.info("Proxy server started.")
openapi_tags = [
    {
        "name": "config",
        "description": "Config from yaml file",
    },
    {
        "name": "start",
        "description": "Starts the proxy server",
    }
]

app = FastAPI(openapi_tags=openapi_tags)

@app.get("/api/config", tags=["config"])
async def read_config():
    """Return config from yaml file"""
    return config

@app.get("/api/start")
async def start():
    """Starts the proxy server"""
    global httpd
    target_url = "http://example.com"
    port = int(config['port'])
    log.info(f"Starting server for {target_url} on port {port}")
    server_manager.stop()
    server_manager._target_url = target_url
    server_manager.run()
    return {"status": "Server started"}

@app.get("/api/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    """Return item_id and q"""
    return {"item_id": item_id, "q": q}

# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
