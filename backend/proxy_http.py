from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import logging
from socketserver import ThreadingMixIn
import threading
from typing import Optional
from urllib.parse import urlparse
from pydantic import BaseModel
import requests

from storage import Storage
import model
from datetime import datetime

class ProxyHTTP(ThreadingMixIn, SimpleHTTPRequestHandler):
    """Serwer proxy"""
    def __init__(self, *args, **kwargs):
        self.target_url = kwargs.pop('target_url', 'https://example.com')
        self._storage = Storage()
        print(f"Proxy for {self.target_url}")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Wykonanie zapytania GET do serwera docelowego"""
        print(f"GET {self.target_url}{self.path}") 
        req = model.Request(url=self.path, method="GET")
        response = requests.get(self.target_url + self.path, headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_POST(self):
        """Wykonanie zapytania POST do serwera docelowego"""
        print(f"POST {self.target_url}{self.path}")
        req = model.Request(url=self.path, method="POST")
        response = requests.post(self.target_url + self.path, data=self._create_data(), headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_PUT(self):
        """Wykonanie zapytania PUT do serwera docelowego"""
        print(f"PUT {self.target_url}{self.path}")
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

    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        self.timeout = 1
        while not self.stop:
            self.handle_request()
            

class ServerManager:
    """Startuje i zatrzymuje serwer http"""
    def __init__(self, port: int = 8999, target_url: str = 'https://example.com') -> None:
        self._port = port
        self._target_url = target_url
        self._httpd = None
        self._thread = None
        self._log = logging.getLogger(__name__)

    def run(self, port: int = None, target_url: str = None) -> StoppableHttpServer:
        if port:
            self._port = port
        if target_url:
            self._target_url = target_url
        server_address = ('', self._port)

        def handler(*args, **kwargs):
            return ProxyHTTP(*args, target_url=self._target_url, **kwargs)
        
        self._httpd = StoppableHttpServer(server_address, handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, name="HttpServer", daemon=True)
        self._thread.start()
        self._log.info(f'Started http proxy on port {self._port} => {self._target_url}')
        return self._httpd

    def stop(self):
        if self._httpd:
            self._log.debug("Stopping server ...")
            self._httpd.stop = True
            self._httpd.server_close()
            self._thread.join()
            self._httpd = None
            self._log.info("Server stopped.")

    def get_status(self):
        return Status(**{
            "status" : "working" if self._httpd else "sopped",
            "port" : self._port,
            "target_url" : self._target_url
        })
    
class Status(BaseModel):
    status: str
    port: Optional[int]
    target_url: Optional[str]