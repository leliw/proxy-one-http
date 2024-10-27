
from .html_element import HtmlElement


class HtmlForm(HtmlElement):
    """Represents HTML form."""

    def get_values(self) -> dict[str, str]:
        """Returns values from form (default values or hidden input values)"""
        ret = {}
        for i in self.find_all("input"):
            name = i.attrs.get("name")
            value = i.attrs.get("value")
            if name and value:
                ret[name] = value
        return ret
    
    def set_value(self, input_name: str, value: str) -> None:
        """Replaces value in input with given name"""
        self.find("input", {"name": input_name}).attrs["value"] = value