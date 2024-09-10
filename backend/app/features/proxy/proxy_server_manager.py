import logging
import threading

from app.config import UserConfig
from storage.directory_storage import DirectoryStorage

from .proxy_model import Status
from .stoppable_http_server import StoppableHttpServer
from .proxy_http import ProxyHTTP


class ProxyServerManager:
    """Startuje i zatrzymuje serwer http"""

    def __init__(self, storage_base_path: str) -> None:
        self._port = None
        self._target_url = None
        self._storage_base_path = storage_base_path
        self._httpd = None
        self._thread = None
        self._log = logging.getLogger(__name__)

    def start(self, config: UserConfig) -> Status:
        """Starts proxy server"""
        self._port = config.port
        self._target_url = config.target_url
        sub_path = self._target_url.split("//")[-1].replace("/", "_")
        self._storage = DirectoryStorage(
            base_path=f"{self._storage_base_path}/{sub_path}"
        )
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
