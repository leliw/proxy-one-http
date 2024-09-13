"""Stores data on disk in json files"""

import logging
import os
import json
from pathlib import Path
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
        full_path = self._key_to_full_path(key)
        self._log.debug("put: %s (%s)", key, full_path)
        json_str = value.model_dump_json(by_alias=True, indent=2, exclude_none=True)
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(json_str)

    def get(self, key: str) -> T:
        self._log.debug("get %s", key)
        full_path = self._key_to_full_path(key)
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                r = json.load(file)
            return self.clazz.model_validate(r)
        except FileNotFoundError:
            return None

    def keys(self) -> Iterator[str]:
        self._log.debug("keys -> start %s", self.folder_path)
        start_index = len(str(self.folder_path)) + 1
        if self.subfolder_characters:
            end_index = self.subfolder_characters + 1
        else:
            end_index = None
        for root, _, files in os.walk(self.folder_path):
            self._log.debug("keys -> walk %s %d", root, len(files))
            if Path(f"{root}.json").is_file() and root != str(self.folder_path):
                # If exists json file wtith the same name as directory
                # and it's not root folder
                # - skip it - it's subcollection
                pass
            else:
                folder = root[start_index:-end_index] if end_index else root[start_index:]
                for file in files:
                    k = f"{folder}/{file}" if folder else file
                    self._log.debug("keys: %s", k)
                    yield k[:-5] if k.endswith(".json") else k
        self._log.debug("keys <- end")

    def delete(self, key: str) -> None:
        self._log.debug("delete %s", key)
        full_path = self._key_to_full_path(key)
        os.remove(full_path)

    def _key_to_full_path(self, key: str) -> str:
        return self._create_file_path(key)
