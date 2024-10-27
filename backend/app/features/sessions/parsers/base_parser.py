from abc import ABC
from typing import Any, List


class BaseParser(ABC):
    variable_fixed_value = "(session_variable)"
    """Base class for all parsers"""

    @classmethod
    def is_applicable(cls, headers: dict[str, Any]) -> bool:
        """The parser is applicable to the given content type"""
        pass

    @classmethod
    def parse(cls, content: str) -> tuple[str, dict]:
        """Parse content and returns fromatent conent and dictionary of values (if is applicable)"""
        pass

    @classmethod
    def replace_variables(cls, variables: List[str], body: str) -> str:
        """Replace variables in body with fixed value. Further comparison won't show the difference"""
        return body
