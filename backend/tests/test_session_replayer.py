import pytest

from app.features.sessions.session_model import Session, SessionRequest
from app.features.sessions.session_replayer import SessionReplayer


@pytest.fixture
def request1():
    request = SessionRequest(url="/", method="GET")
    request.response_headers = {"Content-Type": "text/html; charset=utf-8"}
    request.set_response_body(
        "text/html; charset=utf-8",
        b"""
<html>
 <body>
  <form action="./Login.aspx" id="aspnetForm" method="post" name="aspnetForm">
   <input id="__LASTFOCUS" name="__LASTFOCUS" type="hidden" value=""/>
   <input id="session_id" name="session_id" type="hidden" value="123"/>
  </form>
 </body>
</html>                         
""",
    )
    return request


@pytest.fixture
def request2():
    request = SessionRequest(url="/login.aspx", method="POST")
    request.request_body_form = {"session_id": "(session_variable)"}
    return request


@pytest.fixture
def session():
    return Session(target_url="http://example.com", variables=["session_id"])


def test_extract_variables_from_responsse_body_form_values(request1):
    """Tests extraction defined session variables from response"""
    # Given: variable is defined
    session = Session(target_url="http://example.com", variables=["session_id"])
    # Given: response contain HTML from with field named like variable
    sr = SessionReplayer(session, [request1])

    # When: Response is paresed
    sr._parse_response_variables(request1)

    # Then: Replayer can return map of variables
    assert {"session_id": "123"} == sr._variables


def test_replace_variables_in_html_from_response(request1):
    """Tests replacement defined session variables in HTML from response body"""
    # Given: variable is defined
    session = Session(target_url="http://example.com", variables=["session_id"])
    # Given: response contain HTML from with field named like variable
    sr = SessionReplayer(session, [request1])

    # When: Response is cleaned
    sr.clean_request(request1)

    # Then: response_body_str has replaced variable
    expected = """
<html>
 <body>
  <form action="./Login.aspx" id="aspnetForm" method="post" name="aspnetForm">
   <input id="__LASTFOCUS" name="__LASTFOCUS" type="hidden" value=""/>
   <input id="session_id" name="session_id" type="hidden" value="(session_variable)"/>
  </form>
 </body>
</html>                         
"""
    assert expected.strip() == request1.response_body_str.strip()



def test_create_replay_request_with_variable(session, request2):
    """Test creation replay request with rerplaced variables"""
    # Given: Session with variables
    # Given: Request with Contnet-Type: x-www-form-urlencoded
    # Given: Replayer with variables values
    sr = SessionReplayer(session, [request2])
    sr._variables = {"session_id": "123"}

    # When: Request is creted
    req = sr._create_replay_request_from(request2)

    # Then: Variable value is replaced
    assert "123" == req.request_body_form["session_id"]
