"""Siple file based storage"""
import glob
import os
import json
import re

class KeyNotExists(Exception):
    """Raised when key is not found"""

class Storage:
    """Stores data on disk (key: value)"""
    def __init__(self, base_path="data"):
        self._base_path = base_path

    def keys(self, sub_path: str = None) -> list[str]:
        """Returns list of keys"""
        full_path = os.path.join(self._base_path, sub_path) if sub_path else self._base_path
        return os.listdir(full_path)

    def put(self, key: str, value: any, sub_path: str = None, file_ext: str = None):
        """Save value on disk"""
        if isinstance(value, bytes):
            file_ext = file_ext if file_ext else "bin"
            with open(self._create_file_path(sub_path, key, file_ext), 'bw') as file:
                file.write(value)
        elif isinstance(value, str):
            file_ext = file_ext if file_ext else "txt"
            with open(self._create_file_path(sub_path, key, file_ext), 'w', encoding="utf-8") as file:
                file.write(value)
        else:
            file_ext = file_ext if file_ext else "json"
            with open(self._create_file_path(sub_path, key, file_ext), 'w', encoding="utf-8") as file:
                json.dump(value, file, indent=4)
    
    def get(self, key: str, sub_path: str = None, file_ext: str = None) -> any:
        """Reads value from disk"""
        if file_ext is None:
            full_path = self._create_file_path(sub_path, key, "*")
            print(full_path)
            files = glob.glob(full_path)
            if not files:
                raise KeyNotExists
            file_ext = os.path.splitext(files[0])
            print(file_ext)
        print(sub_path)
        full_path = self._create_file_path(sub_path, key, file_ext)
        print(full_path)

        if file_ext in ['txt', 'html']:
            with open(full_path, 'r', encoding="utf-8") as file:
                return file.read()
        elif file_ext == "json":
            with open(full_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        else:
            with open(full_path, 'br') as file:
                return file.read()

    def _create_file_path(self, sub_path: str, key: str, file_ext: str) -> str:
        # sub_path = datetime.now().strftime('%Y/%m/%d')
        if sub_path:
            file_name = key
            full_path =  os.path.join(self._base_path, sub_path)
        else:
            sub_path = key.split(" ", maxsplit=2)
            file_name = sub_path.pop()
            full_path = os.path.join(self._base_path, *sub_path)
        os.makedirs(full_path, exist_ok=True)
        sanitized = re.sub(r'[\\/*?:"<>|]', '_', file_name)
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        if file_ext:
            return os.path.join(full_path, sanitized + '.' +file_ext)
        else:
            return os.path.join(full_path, sanitized)
