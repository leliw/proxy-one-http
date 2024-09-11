import logging
import threading

from ampf.base.ampf_base_factory import AmpfBaseFactory
from app.features.sessions import session_model
from app.config import UserConfig

from .proxy_model import Status
from .stoppable_http_server import StoppableHttpServer
from .proxy_http import ProxyHTTP


class ProxyServerManager:
    """Startuje i zatrzymuje serwer http"""

    def __init__(self, factory: AmpfBaseFactory) -> None:
        self._factory = factory
        self._log = logging.getLogger(__name__)

        self._storage = None
        self._target_url = None
        self._port = None
        self._httpd = None
        self._thread = None

    def start(self, config: UserConfig) -> Status:
        """Starts proxy server"""
        self._port = config.port
        self._target_url = config.target_url
        sub_path = self._target_url.split("//")[-1].replace("/", "_")
        self._storage = self._factory.create_storage(f"sessions/{sub_path}", session_model.Request, key_name="file_name")
        server_address = ("", self._port)

        def handler(*args, **kwargs):
            return ProxyHTTP(
                *args, target_url=self._target_url, storage=self._storage, **kwargs
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

    def stop(self) -> Status:
        """Stops proxy server"""
        if self._httpd:
            self._log.debug("Stopping server ...")
            self._httpd.stop = True
            self._httpd.server_close()
            self._thread.join()
            self._httpd = None
            self._log.info("Server stopped.")
        return self.get_status()

    def get_status(self) -> Status:
        """Returns proxy server status"""
        return Status(
            **{
                "status": "working" if self._httpd else "stopped",
                "port": self._port,
                "target_url": self._target_url,
            }
        )
