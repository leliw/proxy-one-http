import http
import logging
from typing import Iterator
import requests
from deepdiff import DeepDiff
import difflib

from app.features.sessions.parsers import HtmlParser

from app.features.sessions.parsers.asp_net_parser import AspNetParser
from app.features.sessions.session_model import (
    Session,
    SessionReplayRequest,
    SessionRequest,
)


class SessionReplayer:
    """Replays session"""

    def __init__(self, session: Session, requests: Iterator[SessionRequest]):
        self.session = session
        self.requests = requests
        self._variables = {}
        self._log = logging.getLogger(__name__)

    def replay(self) -> Iterator[SessionReplayRequest]:
        """Starts replay procedure"""
        target_url = self.session.target_url
        cookies = {}
        self._log.info("Replay session %s on %s", self.session.session_id, target_url)
        for org_req in self.requests:
            if not org_req.disabled:
                self._log.debug(org_req.status_code)
                req = self._create_replay_request_from(org_req)
                cookies = self._update_request_cookies(cookies, req)

                resp = self.call_request(target_url, req, cookies)
                cookies = self._update_response_cookies(cookies, resp)
                req.set_response(resp)
                self._parse_response_variables(req)
                self.compare_reqests(org_req, req)
                yield req

    def _create_replay_request_from(
        self, org_req: SessionRequest
    ) -> SessionReplayRequest:
        """Creates request from  oryginal request and replaces existing variables"""
        ret = SessionReplayRequest.from_request(org_req)
        if ret.request_body_form:
            for k, v in self._variables.items():
                if k in ret.request_body_form.keys():
                    ret.request_body_form[k] = v
        return ret

    def _update_request_cookies(self, cookies: dict, req: SessionReplayRequest) -> dict:
        """Gets request cookies and update with session cookies"""
        if "Cookie" in req.request_headers.keys():
            c = http.cookies.SimpleCookie()
            c.load(req.request_headers["Cookie"])
            ret = {key: value.value for key, value in c.items()}
            if ret:
                for k, v in cookies.items():
                    ret[k] = v
                return ret
        return cookies

    def call_request(
        self, target_url: str, req: SessionRequest, cookies: dict
    ) -> requests.Response:
        """Calls given request"""
        self._log.debug("(%s) %s ... ", req.method, req.url)
        req.request_headers["Cookie"] = "; ".join(
            f"{key}={value}" for key, value in cookies.items()
        )
        resp = requests.request(
            req.method,
            f"{target_url}{req.url}",
            headers=req.request_headers,
            data=req.request_body_form
            or req.request_body_str
            or req.request_body_bytes,
            cookies=cookies,
            allow_redirects=False
        )
        self._log.info("(%s) %s => %d", req.method, req.url, resp.status_code)
        return resp

    def _update_response_cookies(self, cookies: dict, resp: requests.Response) -> dict:
        """Update session cookies dictionary with returned in response"""
        for k, v in resp.cookies.get_dict().items():
            cookies[k] = v
        return cookies

    def _parse_response_variables(self, req: SessionRequest) -> None:
        """Parse response body form, remeber values of variables defined in session"""
        if req.response_body_form_values:
            for k in self.session.variables:
                if k in req.response_body_form_values.keys():
                    v = req.response_body_form_values[k]
                    self._variables[k] = v

    def compare_reqests(self, old: SessionRequest, new: SessionReplayRequest):
        """Porównianie oryginalnego requestu i jego ponownego odtworzenia"""
        old = SessionRequest(**old.model_dump())
        new = SessionReplayRequest(**new.model_dump())
        o = self.clean_request(old).model_dump()
        n = self.clean_request(new).model_dump()

        diff = DeepDiff(o, n, ignore_private_variables=False)
        for key, val in diff.get("values_changed", {}).items():
            to = val.get("old_value", "")
            tn = val.get("new_value", "")
            if (
                isinstance(to, str)
                and isinstance(tn, str)
                and max(len(to), len(tn)) > 255
            ):
                diff = difflib.unified_diff(
                    to.splitlines(),
                    tn.splitlines(),
                    lineterm="",
                    fromfile="old",
                    tofile="new",
                )
                diff = "\n".join(diff)
            else:
                diff = f"-{to}\n+{tn}"
            self._log.debug(f"{key}\n" + diff)
            if not new.diff_dict:
                new.diff_dict = {}
            new.diff_dict[key] = diff
            if not new.diff:
                new.diff = ""
            new.diff += f"{key}\n" + diff

    def clean_request(
        self, r: SessionRequest | SessionReplayRequest
    ) -> SessionRequest | SessionReplayRequest:
        """Usuwa dane które zmieniają się zawsze lub skopiowane z nagłówka i nie ma sensu ich porównywać"""
        for key in ["req_id", "start", "end", "resp_content_length"]:
            setattr(r, key, None)
        for key in ["Date"]:
            r.response_headers.pop(key, None)

        if r.response_body_form_values:
            replaced = False
            for k in self.session.variables:
                if k in r.response_body_form_values.keys():
                    r.response_body_form_values[k] = "(session_variable)"
                    replaced = [k]
            # Replace extracted variables with fixed value
            if replaced:
                if HtmlParser.is_applicable(r.response_headers):
                    r.response_body_str = HtmlParser.replace_variables(
                        self.session.variables, r.response_body_str
                    )
                elif AspNetParser.is_applicable(r.response_headers):
                    r.response_body_str = AspNetParser.replace_variables(
                        self.session.variables, r.response_body_str
                    )

        if r.request_body_form:
            for k, v in self._variables.items():
                if k in r.request_body_form.keys():
                    r.request_body_form[k] = "(session_variable)"
        return r
