"""Siple file based storage"""
import glob
import logging
import os
import json
import re

class KeyNotExists(Exception):
    """Raised when key is not found"""

class BasicStorage:
    """Stores data on disk (key: value)"""
    def __init__(self, base_path="data"):
        self._base_path = base_path
        self._log = logging.getLogger(__name__)

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
            try:
                file_ext = self._find_file_ext(sub_path, key)
            except KeyNotExists:
                return None
        full_path = self._create_file_path(sub_path, key, file_ext)

        if file_ext in ['txt', 'html']:
            with open(full_path, 'r', encoding="utf-8") as file:
                return file.read()
        elif file_ext == "json":
            with open(full_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        else:
            with open(full_path, 'br') as file:
                return file.read()

    def delete(self, key: str, sub_path: str = None, file_ext: str = None) -> None:
        """Delete file from disk (value from storage)"""
        if file_ext is None:
            file_ext = self._find_file_ext(sub_path, key)
        full_path = self._create_file_path(sub_path, key, file_ext)
        os.remove(full_path)

    def _create_file_path(self, sub_path: str, key: str, file_ext: str) -> str:
        """Create file path for given key and sub_path"""
        if sub_path:
            file_name = self._evaluate_file_name(key)
        else:
            sub_path, file_name = self._evaluate_sub_path_and_file_name(key)
        if sub_path:
            full_path =  os.path.join(self._base_path, sub_path)
        else:
            full_path = self._base_path
        os.makedirs(full_path, exist_ok=True)
        if file_ext:
            return os.path.join(full_path, file_name + '.' +file_ext)
        else:
            return os.path.join(full_path, file_name)

    def _evaluate_sub_path_and_file_name(self, key: str) -> tuple[str, str]:
        sub_paths = key.split(" ", maxsplit=2)
        file_name = self._evaluate_file_name(sub_paths.pop())
        sub_path = os.path.join(*sub_paths) if sub_paths else None
        return (sub_path, file_name)
    
    def _evaluate_file_name(self, key: str) -> str:
        """Evaluate file name for key"""
        sanitized = re.sub(r'[\\/*?:"<>|]', '_', key)
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        return sanitized

    def _find_file_ext(self, sub_path: str, key: str) -> str:
        """Find file extension for given key"""
        full_path = self._create_file_path(sub_path, key, "*")
        files = glob.glob(full_path)
        self._log.debug(files)
        if not files:
            raise KeyNotExists
        file_ext = os.path.splitext(files[0])[1][1:]
        self._log.debug(file_ext)
        return file_ext
