import json
from typing import Optional
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from datetime import datetime


class Request(BaseModel):
    """Model for request sotored in JSON format"""
    start: datetime = Field(default_factory=lambda: datetime.now())
    end: Optional[datetime] = None
    url: str
    method: str
    status_code: Optional[int] = None
    request_headers: dict = {}
    request_body_form: Optional[dict] = None
    request_body_str: Optional[str] = None
    request_body_bytes: Optional[bytes] = None
    response_headers: dict = {}
    response_body_json: Optional[dict] = None
    response_body_str: Optional[str] = None
    response_body_bytes: Optional[bytes] = None

    def set_reqest_body(self, content_type: str, body: bytes | None):
        content_type = content_type.lower() if body else None
        if body and "charset=utf-8" in content_type:
            body_str = body.decode('utf-8')
            if "application/x-www-form-urlencoded" in content_type:
                body_dict = parse_qs(body_str)
                for key in body_dict.keys():
                    if isinstance(body_dict[key], list) and len(body_dict[key]) == 1:
                        body_dict[key] = body_dict[key][0]
                self.request_body_form = {k: body_dict[k] for k in sorted(body_dict)}
            else:
                self.request_body_str = body_str
        else:
            self.request_body_bytes = body

    def set_response_body(self, content_type: str, body: bytes | None):
        content_type = content_type.lower() if body else None
        if body and "charset=utf-8" in content_type:
            body_str = body.decode('utf-8')
            if "application/json" in content_type or "text/json" in content_type:
                body_dict = json.loads(body_str)
                self.response_body_json = body_dict
            elif "text/html" in content_type:
                soup = BeautifulSoup(body_str, 'html.parser')
                body_str = soup.prettify()
                self.response_body_str = body_str.replace("\r", "")
            else:
                self.response_body_str = body_str
        elif body and content_type.startswith("text/"):
            self.response_body_str = body
        else:
            # self.response_body_bytes = body
            pass
