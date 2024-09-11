import logging
import threading

from app.config import UserConfig
from app.features.sessions.session_service import SessionService

from .proxy_model import ProxyStatus
from .stoppable_http_server import StoppableHttpServer
from .proxy_http import ProxyHTTP


class ProxyServerManager:
    """Startuje i zatrzymuje serwer http"""

    def __init__(self, session_service: SessionService) -> None:
        self.session_serivce = session_service
        self._log = logging.getLogger(__name__)

        self._target_url = None
        self._port = None
        self._httpd = None
        self._thread = None

    def start(self, config: UserConfig) -> ProxyStatus:
        """Starts proxy server"""
        self._port = config.port
        self._target_url = config.target_url
        server_address = ("", self._port)

        def handler(*args, **kwargs):
            return ProxyHTTP(
                *args,
                target_url=self._target_url,
                session_serivce=self.session_serivce,
                **kwargs,
            )

        self._httpd = StoppableHttpServer(server_address, handler)
        self._thread = threading.Thread(
            target=self._httpd.serve_forever, name="HttpServer", daemon=True
        )
        self._thread.start()
        self._log.info(
            "Started http proxy on port %d => %s", self._port, self._target_url
        )
        return self.get_status()

    def stop(self) -> ProxyStatus:
        """Stops proxy server"""
        if self._httpd:
            self._log.debug("Stopping server ...")
            self._httpd.stop = True
            self._httpd.server_close()
            self._thread.join()
            self._httpd = None
            self._log.info("Server stopped.")
        return self.get_status()

    def get_status(self) -> ProxyStatus:
        """Returns proxy server status"""
        return ProxyStatus(
            **{
                "status": "working" if self._httpd else "stopped",
                "port": self._port,
                "target_url": self._target_url,
            }
        )
