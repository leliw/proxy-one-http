import logging
import threading

from app.features.sessions.session_service import SessionService

from .proxy_model import ProxySettings, ProxyStatus
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

    def start(self, proxySettings: ProxySettings) -> ProxyStatus:
        """Starts proxy server"""
        self._port = proxySettings.port
        self._target_url = proxySettings.target_url
        server_address = ("", self._port)
        self.session_serivce.start_session(
            proxySettings.target_url, description=proxySettings.session_description
        )

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
        self.session_serivce.stop_session()
        return self.get_status()

    def is_stopped(self) -> bool:
        return not bool(self._httpd)

    def get_status(self) -> ProxyStatus:
        """Returns proxy server status"""
        return ProxyStatus(
            **{
                "status": "stopped" if self.is_stopped() else "working",
                "port": self._port,
                "target_url": self._target_url,
            }
        )
