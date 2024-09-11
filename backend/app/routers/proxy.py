from typing import Annotated
from fastapi import APIRouter, Depends

from app.config import UserConfig
from app.features.proxy.proxy_model import Settings, Status
from app.features.proxy.proxy_server_manager import ProxyServerManager
from app.routers.sessions import SessionServiceDep


router = APIRouter(tags=["Proxy server"])
service = None


def get_service(session_service: SessionServiceDep) -> ProxyServerManager:
    global service
    if not service:
        service = ProxyServerManager(session_service)
    return service


ServiceDep = Annotated[ProxyServerManager, Depends(get_service)]


@router.post("/start")
async def proxy_start(service: ServiceDep, settings: Settings):
    """Starts the proxy server"""
    return service.start(UserConfig(port=settings.port, target_url=settings.target_url))


@router.post("/stop")
async def proxy_stop(service: ServiceDep):
    """Stops the proxy server"""
    return service.stop()


@router.get("/status")
async def proxy_status(service: ServiceDep) -> Status:
    """Returns porxy server status"""
    return service.get_status()
