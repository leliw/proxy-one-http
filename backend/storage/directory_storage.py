"""
Simple file based storage (key: value)
where key is a file name and value is a file content.
The key can contain any number "/" to create a tree of directories.
"""
import logging
import os
from pathlib import Path


from .basic_storage import BasicStorage


class DirectoryStorage(BasicStorage):
    """Stores data on disk in directories (tree)"""
    def __init__(self, base_path="data"):
        super().__init__(base_path)
        self._log = logging.getLogger(__name__)

    def get_directory_tree(self, sub_path: str = None) -> list:
        """Returns tree of directories in storage"""
        sub_path = Path(sub_path if sub_path else self._base_path)
        if sub_path.is_dir():
            children = [self._get_directory_children(e) for e in sub_path.iterdir()]
            if children:
                return children
        return []
    
    def _get_directory_children(self, sub_path: str = None) -> dict|None:
        sub_path = Path(sub_path)
        if sub_path.is_dir():
            children = [self._get_directory_children(e) for e in sub_path.iterdir()]
            ret = {"name": sub_path.name}
            if children:
                ret["children"] = children
            return ret
        else:
            return None

    def _evaluate_sub_path_and_file_name(self, key: str) -> tuple[str, str]:
        """Returns sub_path and file_name from key where sub_path is a part of key before last '/' and file_name is a part after last '/'"""
        sub_paths = key.split("/", maxsplit=2)
        file_name = self._evaluate_file_name(sub_paths.pop())
        sub_path = os.path.join(*sub_paths) if sub_paths else None
        return (sub_path, file_name)