from typing import Any, List

from .base_parser import BaseParser
from .html_parser import HtmlPage


class HtmlParser(BaseParser):
    """Parser for HTML response. Extracts from values"""
    @classmethod
    def is_applicable(cls, headers: dict[str, Any]) -> bool:
        return "text/html" in headers.get("Content-Type")

    @classmethod
    def parse(cls, content: str) -> tuple[str, dict]:
        page = HtmlPage(content)
        ret_str = page.prettify()
        ret_dict = None
        try:
            form = next(page.find_all_forms())
            if form:
                ret_dict = form.get_values()
        except StopIteration:
            pass
        return (ret_str, ret_dict)

    @classmethod
    def replace_variables(cls, variables: List[str], body: str) -> str:
        page = HtmlPage(body)
        form = next(page.find_all_forms())
        for n in variables:
            form.set_value(n, cls.variable_fixed_value)
        return page.prettify()
