from typing import Annotated
from fastapi import APIRouter, Depends

from app.config import UserConfig
from app.features.proxy.proxy_model import ProxySettings, ProxyStatus
from app.features.proxy.proxy_server_manager import ProxyServerManager
from app.routers.sessions import SessionServiceDep


router = APIRouter(tags=["Proxy server"])
# The same object has to be accessible between requests
proxy_service_manager: ProxyServerManager = None

def get_service(session_service: SessionServiceDep) -> ProxyServerManager:
    global proxy_service_manager
    if not proxy_service_manager or proxy_service_manager.is_stopped():
        proxy_service_manager = ProxyServerManager(session_service)
        # For tests service is recreated when is stopped - storage changes root dir between tests
    return proxy_service_manager


ServiceDep = Annotated[ProxyServerManager, Depends(get_service)]


@router.post("/start")
async def proxy_start(service: ServiceDep, settings: ProxySettings):
    """Starts the proxy server"""
    return service.start(UserConfig(port=settings.port, target_url=settings.target_url))


@router.post("/stop")
async def proxy_stop(service: ServiceDep):
    """Stops the proxy server"""
    return service.stop()


@router.get("/status")
async def proxy_status(service: ServiceDep) -> ProxyStatus:
    """Returns porxy server status"""
    return service.get_status()
