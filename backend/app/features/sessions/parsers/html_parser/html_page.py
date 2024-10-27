from typing import Iterator
from .html_element import HtmlElement
from .html_form import HtmlForm


class HtmlPage(HtmlElement):
    """Represents HTML Page"""

    def find_all_forms(self) -> Iterator[HtmlForm]:
        """Returns all form from page."""
        for f in self.decorated.find_all("form"):
            yield HtmlForm(f)
