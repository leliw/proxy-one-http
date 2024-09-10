from http.server import ThreadingHTTPServer


class StoppableHttpServer(ThreadingHTTPServer):
    """http server that reacts to self.stop flag"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop = False

    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until stopped."""
        self.timeout = poll_interval
        while not self.stop:
            self.handle_request()
