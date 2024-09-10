"""Stores data on disk in json files"""

import logging
import os
import json
from typing import Iterator, Type

from ..base import BaseStorage
from .file_storage import FileStorage


class JsonMultiFilesStorage[T](BaseStorage[T], FileStorage):
    """Stores data on disk in json files. Each item is stored in its own file"""

    def __init__(
        self,
        path_name: str,
        clazz: Type[T],
        key_name: str = None,
        subfolder_characters: int = None,
    ):
        BaseStorage.__init__(self, clazz, key_name)
        FileStorage.__init__(
            self,
            folder_name=path_name,
            default_ext="json",
            subfolder_characters=subfolder_characters,
        )
        self._log = logging.getLogger(__name__)

    def put(self, key: str, value: T) -> None:
        json_str = value.model_dump_json(by_alias=True, indent=2, exclude_none=True)
        with open(self._key_to_full_path(key), "w", encoding="utf-8") as file:
            file.write(json_str)

    def get(self, key: str) -> T:
        full_path = self._key_to_full_path(key)
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                r = json.load(file)
            return self.clazz.model_validate(r)
        except FileNotFoundError:
            return None

    def keys(self) -> Iterator[str]:
        start_index = len(str(self.folder_path))+1
        if self.subfolder_characters:
            end_index = self.subfolder_characters+1
        else:
            end_index = 1
        for root, _, files in os.walk(self.folder_path):
            folder = root[start_index:-end_index]    
            for file in files:
                k = f"{folder}/{file}" if folder else file
                yield k[:-5] if k.endswith(".json") else k

    def delete(self, key: str) -> None:
        full_path = self._key_to_full_path(key)
        os.remove(full_path)

    def _key_to_full_path(self, key: str) -> str:
        return self._create_file_path(key)
