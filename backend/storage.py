import os
from datetime import datetime
import json
import re

class Storage:
    
    def __init__(self, base_path="data", file_extension="json"):
        self._base_path = base_path
        self._file_extension = file_extension

    def put(self, key: str, value: any):
        if isinstance(value, bytes):
            with open(self._create_file_path(key), 'bw') as file:
                file.write(value)
        else:
            with open(self._create_file_path(key), 'w') as file:
                if isinstance(value, str):
                    file.write(value)
                else:
                    json.dump(value, file, indent=4)
    
    def _create_file_path(self, key: str) -> str:
        # sub_path = datetime.now().strftime('%Y/%m/%d')
        sub_path = key.split(" ", maxsplit=2)
        file_name = sub_path.pop()
        full_path = os.path.join(self._base_path, *sub_path)
        os.makedirs(full_path, exist_ok=True)
        sanitized = re.sub(r'[\\/*?:"<>|]', '_', file_name)
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        return os.path.join(full_path, sanitized + '.' + self._file_extension)
