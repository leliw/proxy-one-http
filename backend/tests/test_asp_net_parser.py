from app.features.sessions.parsers import AspNetParser


def test_parse_dict():
    # Given: ASP.NET response
    body_str = "1|#||4|0|hiddenField|__EVENTARGUMENT||192|hiddenField|__VIEWSTATE|/wEPaA8FDzhkY2U5MDk0ZmFmNDdkNRgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUZY3RsMDAkbHNMb2dpblN0YXR1cyRjdGwwMQUZY3RsMDAkbHNMb2dpblN0YXR1cyRjdGwwM8EH/LXysWZYiGh1ElOVpt65ItXpl7RGq72MBNICGWFb|8|hiddenField|__VIEWSTATEGENERATOR|A0C61021|0|asyncPostBackControlIDs|||"

    # When: Response is parsed
    _, d = AspNetParser.parse(body_str)

    # Then: Response is dictionary
    expected = {
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPaA8FDzhkY2U5MDk0ZmFmNDdkNRgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUZY3RsMDAkbHNMb2dpblN0YXR1cyRjdGwwMQUZY3RsMDAkbHNMb2dpblN0YXR1cyRjdGwwM8EH/LXysWZYiGh1ElOVpt65ItXpl7RGq72MBNICGWFb",
        "__VIEWSTATEGENERATOR": "A0C61021",
    }
    assert len(expected) == len(d)
    for k in expected.keys():
        assert expected[k] == d[k]
