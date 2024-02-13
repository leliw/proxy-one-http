from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from socketserver import ThreadingMixIn
import threading
from urllib.parse import parse_qs, urlparse
import requests
import brotli
from storage import Storage
import model
from datetime import datetime

class ProxyHTTP(ThreadingMixIn, SimpleHTTPRequestHandler):
    """Serwer proxy"""
    def __init__(self, *args, **kwargs):
        self.target_url = kwargs.pop('target_url', 'https://example.com')
        self._storage = Storage()
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

def make_server_handler(target_url):
    def handler(*args, **kwargs):
        return ProxyHTTP(*args, target_url=target_url, **kwargs)
    return handler

def run(server_class=HTTPServer, port=8999, target_url='https://example.com'):
    server_address = ('', port)
    handler = make_server_handler(target_url)
    httpd = server_class(server_address, handler)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()