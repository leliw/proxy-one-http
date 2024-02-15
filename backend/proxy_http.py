"""Proxy Server"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import logging
from socketserver import ThreadingMixIn
import threading
from urllib.parse import urlparse
from datetime import datetime
import requests
from pydantic import BaseModel

from storage import Storage
import model

DEFAULT_TARGET_URL = 'https://example.com'

class ProxyHTTP(ThreadingMixIn, SimpleHTTPRequestHandler):
    """Serwer proxy"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_url = kwargs.pop('target_url', DEFAULT_TARGET_URL)  
        self._storage =  kwargs.pop('storage', Storage())
        self._log = logging.getLogger(__name__)
        self._log.debug("Proxy for %s", self.target_url)

    def do_GET(self):
        """Wykonanie zapytania GET do serwera docelowego"""
        self._log.debug("GET %s%s", self.target_url, self.path) 
        req = model.Request(url=self.path, method="GET")
        response = requests.get(self.target_url + self.path, headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_POST(self):
        """Wykonanie zapytania POST do serwera docelowego"""
        self._log.debug("POST %s%s", self.target_url, self.path) 
        req = model.Request(url=self.path, method="POST")
        response = requests.post(self.target_url + self.path, data=self._create_data(), headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_PUT(self):
        """Wykonanie zapytania PUT do serwera docelowego"""
        self._log.debug("PUT %s%s", self.target_url, self.path) 
        req = model.Request(url=self.path, method="PUT")
        response = requests.put(self.target_url + self.path, data=self._create_data(), headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_QUIT (self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def _create_headers(self) -> dict:
        """Pobranie nagłówków aktualnego żądania i zwrócenie ich jako dict"""
        headers = {key: val for key, val in self.headers.items()}
        headers['Host'] = urlparse(self.target_url).netloc
        return headers

    def _create_data(self) -> bytes:
        """Pobranie body aktuanego żadnia i zwrócenie uch jako bytes"""
        content_length = int(self.headers['Content-Length'])
        return self.rfile.read(content_length)
    
    def _save_request(self, req: model.Request, response: requests.Response):
        req.status_code = response.status_code
        req.end = datetime.now()
        req.request_headers = {key: val for key, val in sorted(response.request.headers.items(), key=lambda e: e[0])}
        req.response_headers = {key: val for key, val in sorted(response.headers.items(), key=lambda e: e[0])}
        req.set_reqest_body(req.request_headers.get("Content-Type"), response.request.body)
        req.set_response_body(req.response_headers.get("Content-Type"), response.content)

        file_name = "_".join([
            str(req.start),
            req.method,
            req.url,
            str(req.status_code)
            ])
        self._storage.put(key=file_name, value=req.model_dump_json(indent=4, exclude_none=True))
    
    def _process_response(self, response: requests.Response):
        # Jeśli odpowiedź jest skompresowana, to usuwamy nagłówek Content-Encoding
        # i ustawiamy nagłówek Content-Length na długość treści odpowiedzi
        # (bo jak mam rozkompresowaną odpowiedź, to wysyłam ją bez kompresji)
        content_encoding = response.headers.get('Content-Encoding')
        content = response.content                
        if content_encoding and content_encoding in ["gzip", "br"]:
            del response.headers['Content-Encoding']
            response.headers['Content-Length'] = str(len(content))
            if response.headers.get('Transfer-Encoding'):
                del response.headers['Transfer-Encoding']
        # Ustawienie kodu odpowiedzi
        self.send_response(response.status_code)
        # Przekazanie nagłówków odpowiedzi
        for key, value in response.headers.items():
            #print(F"{key}: {value}")
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content)


class StoppableHttpServer (ThreadingHTTPServer):
    """http server that reacts to self.stop flag"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop = False

    def serve_forever (self, poll_interval=0.5):
        """Handle one request at a time until stopped."""
        self.timeout = poll_interval
        while not self.stop:
            self.handle_request()

class Settings(BaseModel):
    """Proxy server setting"""
    port: int = 8999
    target_url: str = DEFAULT_TARGET_URL

class Status(Settings):
    """Proxy server status"""
    status: str

class ServerManager:
    """Startuje i zatrzymuje serwer http"""
    def __init__(self, port: int = 8999, target_url: str = DEFAULT_TARGET_URL, storage: Storage = Storage()) -> None:
        self._port = port
        self._target_url = target_url
        self._storage = storage
        self._httpd = None
        self._thread = None
        self._log = logging.getLogger(__name__)

    def start(self, port: int = None, target_url: str = None) -> Status:
        """Starts proxy server"""
        if port:
            self._port = port
        if target_url:
            self._target_url = target_url
        server_address = ('', self._port)

        def handler(*args, **kwargs):
            return ProxyHTTP(*args, target_url=self._target_url, storage=self._storage, **kwargs)

        self._httpd = StoppableHttpServer(server_address, handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, name="HttpServer", daemon=True)
        self._thread.start()
        self._log.info('Started http proxy on port %d => %s', self._port, self._target_url)
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
        return Status(**{
            "status" : "working" if self._httpd else "stopped",
            "port" : self._port,
            "target_url" : self._target_url
        })
