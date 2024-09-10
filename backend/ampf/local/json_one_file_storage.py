"""Stores data on disk in json files"""

import logging
import json
from typing import Iterator, Type

from pydantic import BaseModel

from ..base import BaseStorage
from .file_storage import FileStorage

DEF_EXT = "json"


class JsonOneFileStorage[T: BaseModel](BaseStorage[T], FileStorage):
    def __init__(self, file_name: str, clazz: Type[T], key_name: str = None):
        BaseStorage.__init__(self, clazz, key_name)
        FileStorage.__init__(self, default_ext=DEF_EXT)

        if "." not in file_name:
            file_name = f"{file_name}.{DEF_EXT}"
        self.file_name = file_name
        self.file_path = self.folder_path.joinpath(file_name)
        self._log = logging.getLogger(__name__)

    def _load_data(self) -> dict[str, T]:
        try:
            return json.load(open(self.file_path, "r", encoding="utf-8"))
        except FileNotFoundError:
            return {}

    def _save_data(self, data: dict[str, T]) -> None:
        json.dump(
            data,
            open(self.file_path, "w", encoding="utf-8"),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )

    def put(self, key: str, value: T) -> None:
        dv = value.model_dump()
        dv.pop(self.key_name, None)
        data = self._load_data()
        data[key] = dv
        self._save_data(data)

    def get(self, key: str) -> T:
        try:
            data = self._load_data()
            dv = data[key]
            dv[self.key_name] = key
            return self.clazz.model_validate(dv)
        except KeyError:
            return None

    def keys(self) -> Iterator[str]:
        data = self._load_data()
        for k in data.keys():
            yield k

    def delete(self, key: str) -> None:
        data = self._load_data()
        data.pop(key, None)
        self._save_data(data)
