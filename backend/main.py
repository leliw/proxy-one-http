"""Main file for FastAPI server"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pyaml_env import parse_config
import proxy_http

from static_files import static_file_response
from storage.directory_storage import DirectoryStorage
import model

config = parse_config('./config.yaml')

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main_py")

storage = DirectoryStorage(base_path="data/proxy")
server_manager = proxy_http.ServerManager("data/proxy")
server_manager.start()

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
    }
]

app = FastAPI(openapi_tags=openapi_tags)

@app.get("/api/config")
async def read_config():
    """Return config from yaml file"""
    return config

@app.post("/api/proxy/start", tags=["Proxy"])
async def proxy_start(settings: proxy_http.Settings):
    """Starts the proxy server"""
    return server_manager.start(port=settings.port, target_url=settings.target_url)

@app.post("/api/proxy/stop", tags=["Proxy"])
async def proxy_stop():
    """Stops the proxy server"""
    return server_manager.stop()

@app.get("/api/proxy/status", tags=["Proxy"])
async def proxy_status() -> proxy_http.Status:
    """Returns porxy server status"""
    return server_manager.get_status()

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
