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

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Startup event"""
    log.debug("Startup event")
    def run():
        proxy_http.run(target_url=config['target_url'], port=int(config['port']))
    threading.Thread(target=run, daemon=True).start()
    log.debug("Startup event end")
    yield
    
openapi_tags = [
    {
        "name": "config",
        "description": "Config from yaml file",
    },
]

app = FastAPI(lifespan=lifespan, openapi_tags=openapi_tags)

@app.get("/api/config", tags=["config"])
async def read_config():
    """Return config from yaml file"""
    return config

@app.get("/api")
async def read_root():
    """Return Hello World"""
    return {"Hello": "World"}

@app.get("/api/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    """Return item_id and q"""
    return {"item_id": item_id, "q": q}

# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
