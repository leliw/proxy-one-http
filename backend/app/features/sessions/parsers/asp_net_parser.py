from typing import Any, List
from .base_parser import BaseParser


class AspNetParser(BaseParser):
    """Parser for ASP.NET response"""

    @classmethod
    def is_applicable(cls, headers: dict[str, Any]) -> bool:
        return (
            "text/plain" in headers.get("Content-Type")
            and headers.get("X-Powered-By") == "ASP.NET"
        )

    @classmethod
    def parse(cls, content: str) -> tuple[str, dict]:
        # It's strange ASP.net response. Something like JSON
        # Let's split it into lines to better recognize differences
        # and also return as JSON
        ret_str = []
        ret_dict = {}
        while content:
            # There are 4 parts for each object splited by "|"
            # 0 - length of 3 part
            # 1 - object type
            # 2 - object name
            # 3 - object value
            # Then there is "|" and next object
            parts = content.split("|", 3)
            len = int(parts.pop(0))
            content = parts[2][len + 1 :]
            # If object value is multiline string, let's format then
            parts[2] = (
                parts[2][:len]
                .replace("\\n", "\n  ")
                .replace("\\r", "")
                .replace("\\t", "\t")
            )
            # Return object as fromated string
            ret_str.append("|".join(parts))
            if "hiddenField" == parts[0]:
                # Return object as dict with values
                ret_dict[parts[1]] = parts[2]
        return ("\n".join(ret_str), ret_dict)

    @classmethod
    def replace_variables(cls, variables: List[str], body: str) -> str:
        lines = body.split("\n")
        ret = []
        for line in lines:
            for n in variables:
                if line.startswith(f"hiddenField|{n}|"):
                    parts = line.split("|")
                    parts[2] = cls.variable_fixed_value
                    line = "|".join(parts)
            ret.append(line)
        return "\n".join(ret)
