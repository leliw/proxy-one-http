import json
from typing import Optional
from urllib.parse import parse_qs
import uuid
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from datetime import datetime, date


class Session(BaseModel):
    session_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    session_date: Optional[date] = Field(default_factory=lambda: datetime.now().date())
    target_url: str
    requests_cnt: Optional[int] = 0
    description: Optional[str] = None


class SessionRequest(BaseModel):
    """Model for request stored in JSON format"""

    start: datetime = Field(default_factory=datetime.now)
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
        """Formats and sets request_body"""
        content_type = content_type.lower() if body else None
        if body and "charset=utf-8" in content_type:
            body_str = body.decode("utf-8")
            if "application/x-www-form-urlencoded" in content_type:
                body_dict = parse_qs(body_str)
                for el in body_dict.items():
                    if isinstance(el, list) and len(el) == 1:
                        el = el[0]
                self.request_body_form = {k: body_dict[k] for k in sorted(body_dict)}
            else:
                self.request_body_str = body_str
        else:
            self.request_body_bytes = body

    def set_response_body(self, content_type: str, body: bytes | None):
        """Formats and sets response body"""
        content_type = content_type.lower() if body else None
        if body and "charset=utf-8" in content_type:
            body_str = body.decode("utf-8")
            if "application/json" in content_type or "text/json" in content_type:
                body_dict = json.loads(body_str)
                self.response_body_json = body_dict
            elif "text/html" in content_type:
                soup = BeautifulSoup(body_str, "html.parser")
                body_str = soup.prettify()
                self.response_body_str = body_str.replace("\r", "")
            else:
                self.response_body_str = body_str
        elif body and content_type.startswith("text/"):
            self.response_body_str = body
        else:
            # self.response_body_bytes = body
            pass
