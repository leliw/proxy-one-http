from typing import Annotated
from fastapi import APIRouter, Depends

import app.proxy_http as proxy_http


router = APIRouter(tags=["Proxy server"])
service = None
def get_service():
    global service
    if not service:
         service = proxy_http.ServerManager("data/proxy")
    return service

ServiceDep = Annotated[proxy_http.ServerManager, Depends(get_service)]


@router.post("/start")
async def proxy_start(service: ServiceDep, settings: proxy_http.Settings):
    """Starts the proxy server"""
    return service.start(port=settings.port, target_url=settings.target_url)


@router.post("/stop")
async def proxy_stop(service: ServiceDep):
    """Stops the proxy server"""
    return service.stop()


@router.get("/status")
async def proxy_status(service: ServiceDep) -> proxy_http.Status:
    """Returns porxy server status"""
    return service.get_status()
