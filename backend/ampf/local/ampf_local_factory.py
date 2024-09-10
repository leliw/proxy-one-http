from functools import lru_cache
from pathlib import Path
from typing import Type
from pydantic import BaseModel

from ..base.ampf_base_factory import AmpfBaseFactory
from ..base.base_storage import BaseStorage
from ..local.file_storage import FileStorage, StrPath
from .json_multi_files_storage import JsonMultiFilesStorage
from .json_one_file_storage import JsonOneFileStorage


class AmpfLocalFactory(AmpfBaseFactory):
    def __init__(self, root_dir_path: StrPath):
        FileStorage._root_dir_path = Path(root_dir_path)

    @lru_cache(maxsize=64)
    def create_storage[T: BaseModel](
        self, collection_name: str, clazz: Type[T], key_name: str = None
    ) -> BaseStorage[T]:
        return JsonMultiFilesStorage(
            path_name=collection_name, clazz=clazz, key_name=key_name
        )

    @lru_cache(maxsize=64)
    def create_compact_storage[T: BaseModel](
        self, collection_name: str, clazz: Type[T], key_name: str = None
    ) -> BaseStorage[T]:
        return JsonOneFileStorage(
            file_name=collection_name, clazz=clazz, key_name=key_name
        )
