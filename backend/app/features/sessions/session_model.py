from __future__ import annotations
import json
from typing import Any, List, Optional, Self
from urllib.parse import parse_qs
import uuid6
from pydantic import BaseModel, Field, computed_field
from datetime import datetime
import requests

from .parsers import AspNetParser, HtmlParser



class Session(BaseModel):
    session_id: Optional[str] = Field(default_factory=lambda: str(uuid6.uuid6()))
    session_date: Optional[str] = Field(default_factory=lambda: str(datetime.now()))
    target_url: str
    requests_cnt: Optional[int] = 0
    description: Optional[str] = None
    variables: Optional[List[str]] = Field(default_factory=list)
    req_ids: Optional[List[str]] = Field(default_factory=list)


class SessionReplayHeader(BaseModel):
    replay_id: Optional[str] = Field(default_factory=lambda: str(uuid6.uuid6()))
    replay_date: Optional[str] = Field(default_factory=lambda: str(datetime.now()))
    session_id: str
    requests_cnt: Optional[int] = 0
    description: Optional[str] = None


class SessionReplay(SessionReplayHeader):
    req_ids: Optional[List[str]] = Field(default_factory=list)


class SessionRequestHeader(BaseModel):
    req_id: Optional[str] = Field(default_factory=lambda: str(uuid6.uuid6()))
    start: datetime = Field(default_factory=datetime.now)
    end: Optional[datetime] = None
    url: str
    method: str
    status_code: Optional[int] = None
    resp_content_length: Optional[int] = None
    resp_content_type: Optional[str] = None
    cached: Optional[bool] = False
    disabled: Optional[bool] = False
    description: Optional[str] = ""

    @computed_field
    @property
    def duration(self) -> Optional[str]:
        return str(self.end - self.start) if self.end else None


class SessionRequest(SessionRequestHeader):
    """Model for request stored in JSON format"""

    request_headers: dict = {}
    request_body_form: Optional[dict] = None
    request_body_str: Optional[str] = None
    request_body_bytes: Optional[bytes] = None
    response_headers: Optional[dict]= Field(default_factory=lambda:{})
    response_body_json: Optional[dict] = None
    response_body_form_values: Optional[dict] = None
    response_body_str: Optional[str] = None
    response_body_bytes: Optional[bytes] = None

    def copy_request(self) -> Self:
        """Copy only reqest part, response part is none"""
        ret = SessionRequest(
            req_id=self.req_id,
            url=self.url,
            method=self.method,
            request_headers=self.request_headers,
            request_body_str=self.request_body_str or None,
            request_body_form=self.request_body_form or None,
            request_body_bytes=self.request_body_bytes or None,
        )
        return ret

    def _process_response(self, response: requests.Response) -> requests.Response:
        # Jeśli odpowiedź jest skompresowana, to usuwamy nagłówek Content-Encoding
        # i ustawiamy nagłówek Content-Length na długość treści odpowiedzi
        # (bo jak mam rozkompresowaną odpowiedź, to wysyłam ją bez kompresji)
        content_encoding = response.headers.get("Content-Encoding")
        content = response.content
        if content_encoding and content_encoding in ["gzip", "br"]:
            del response.headers["Content-Encoding"]
        response.headers["Content-Length"] = str(len(content))
        if response.headers.get("Transfer-Encoding"):
            del response.headers["Transfer-Encoding"]
        return response

    def set_response(self, response: requests.Response) -> None:
        """Set response part. Sorts headers by names, formats bodies."""
        response = self._process_response(response)
        self.status_code = response.status_code
        if not self.end:
            self.end = datetime.now()
        self.request_headers = {
            key: val
            for key, val in sorted(response.request.headers.items(), key=lambda e: e[0])
        }
        self.response_headers = {
            key: val
            for key, val in sorted(response.headers.items(), key=lambda e: e[0])
        }
        self.set_reqest_body(
            self.request_headers.get("Content-Type"), response.request.body
        )
        self.set_response_body(
            self.response_headers.get("Content-Type"), response.content
        )
        self.resp_content_length = int(self.response_headers.get("Content-Length"))
        self.resp_content_type = self.response_headers.get("Content-Type")
        # If response header contains ETag or Last-Modified -> request can be
        # cahced by client (and is independend from previous requests)
        self.cached = any(
            tag in self.response_headers.keys() for tag in ["ETag", "Last-Modified"]
        )
        # Cached requests aren't replayed by default
        self.disabled = self.cached

    def set_reqest_body(self, content_type: str, body: str):
        """Formats and sets request_body"""
        content_type = content_type.lower() if body else None
        if body:
            if "application/x-www-form-urlencoded" in content_type:
                body_dict = parse_qs(body)
                for k, v in body_dict.items():
                    if isinstance(v, list) and len(v) == 1:
                        body_dict[k] = v[0]
                self.request_body_form = {k: body_dict[k] for k in sorted(body_dict)}
            else:
                self.request_body_str = body.decode("utf-8")

    def set_response_body(self, content_type: str, body: bytes | None):
        """Formats and sets response body"""
        content_type = content_type.lower() if body else None
        if body and "charset=utf-8" in content_type:
            body_str = body.decode("utf-8")
            if "application/json" in content_type or "text/json" in content_type:
                body_dict = json.loads(body_str)
                self.response_body_json = body_dict
            elif HtmlParser.is_applicable(self.response_headers):
                self.response_body_str, self.response_body_form_values = (
                    HtmlParser.parse(body_str)
                )
            elif AspNetParser.is_applicable(self.response_headers):
                self.response_body_str, self.response_body_form_values = (
                    AspNetParser.parse(body_str)
                )
            else:
                self.response_body_str = body_str
        elif body and content_type.startswith("text/"):
            self.response_body_str = body
        else:
            # self.response_body_bytes = body
            pass


class SessionRequestPatch(BaseModel):
    """Definition of SessionRequest properties
    that can be changed by Patch method"""
    disabled: Optional[bool] = None
    description: Optional[str] = None

class SessionReplayRequestHeader(SessionRequestHeader):
    """Data visible in table of SessionReplayRequests"""
    org_status_code: Optional[int] = None
    diff: Optional[str] = None
    diff_dict: Optional[dict[str, Any]] = None

class SessionReplayRequest(SessionReplayRequestHeader, SessionRequest):

    @classmethod
    def from_request(cls, req: SessionRequest):
        """Copy only reqest part, response part is none"""
        ret = SessionReplayRequest(
            req_id=req.req_id,
            url=req.url,
            method=req.method,
            org_status_code=req.status_code,
            request_headers=req.request_headers,
            request_body_str=req.request_body_str or None,
            request_body_form=req.request_body_form or None,
            request_body_bytes=req.request_body_bytes or None,
        )
        return ret

class SessionReplayRequestDto(BaseModel):
    """SessionReplayRequest returned to client.
    
    It contains whole oryginal and replayed requests.
    """
    req_id: str
    url: str
    method: str
    org: SessionRequest
    repl:SessionReplayRequest
    diff: Optional[str] = None
    diff_dict: Optional[dict[str, Any]] = None

    @classmethod
    def create(cls, org: SessionRequest, repl: SessionReplayRequest) -> SessionReplayRequestDto:
        return SessionReplayRequestDto(
            req_id=org.req_id,
            url=org.url,
            method=org.method,
            org=org,
            repl=repl,
            diff=repl.diff,
            diff_dict=repl.diff_dict
        )