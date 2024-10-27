"""Proxy Server"""
import asyncio
from http.server import SimpleHTTPRequestHandler
import logging
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
from datetime import datetime
import requests

from  app.features.sessions.session_model import SessionRequest
from app.features.sessions.session_service import SessionService



class ProxyHTTP(ThreadingMixIn, SimpleHTTPRequestHandler):
    """Serwer proxy"""

    def __init__(self, *args, session_serivce: SessionService, queue: asyncio.Queue, target_url: str, **kwargs):
        self.target_url = target_url
        self.session_service =  session_serivce
        self.queue = queue
        self._log = logging.getLogger(__name__)
        self._log.debug("Proxy for %s", self.target_url)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Wykonanie zapytania GET do serwera docelowego"""
        self._log.debug("GET %s%s", self.target_url, self.path) 
        req = SessionRequest(url=self.path, method="GET")
        response = requests.get(self.target_url + self.path, headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_POST(self):
        """Wykonanie zapytania POST do serwera docelowego"""
        self._log.debug("POST %s%s", self.target_url, self.path) 
        req = SessionRequest(url=self.path, method="POST")
        response = requests.post(self.target_url + self.path, data=self._create_data(), headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def do_PUT(self):
        """Wykonanie zapytania PUT do serwera docelowego"""
        self._log.debug("PUT %s%s", self.target_url, self.path) 
        req = SessionRequest(url=self.path, method="PUT")
        response = requests.put(self.target_url + self.path, data=self._create_data(), headers=self._create_headers(), allow_redirects=False)
        self._process_response(response)
        self._save_request(req, response)

    def _create_headers(self) -> dict:
        """Pobranie nagłówków aktualnego żądania i zwrócenie ich jako dict"""
        headers = {key: val for key, val in self.headers.items()}
        if 'Host' in headers.keys():
            headers['Host'] = urlparse(self.target_url).netloc
        if 'Referer' in headers.keys():
            scheme = urlparse(self.target_url).scheme
            netloc = urlparse(self.target_url).netloc
            path = urlparse(headers['Referer']).path
            headers['Referer'] = f"{scheme}//{netloc}{path}"
        return headers

    def _create_data(self) -> bytes:
        """Pobranie body aktualnego żądnia i zwrócenie ich jako bytes"""
        content_length = int(self.headers['Content-Length'])
        return self.rfile.read(content_length)
    
    def _save_request(self, req: SessionRequest, response: requests.Response):
        """Save request with its respose in session."""
        req.end = datetime.now()
        req.set_response(response)
        self.session_service.add_session_request(req)
        m = f"({req.method}) {req.url} => {req.status_code}"
        self._log.debug(m)
        asyncio.run(self.queue.put(m))
    
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




