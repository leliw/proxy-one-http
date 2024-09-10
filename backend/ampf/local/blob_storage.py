import json
import logging
import os
from pydantic import BaseModel

from .file_storage import FileStorage


class LocalBlobStorage(FileStorage):
    """Zapisuje na dysku dane binarne.

    Args:
        bucket_name: nazwa podkatalogu w który są składowane pliki
        default_ext: domyślne rozszerzenie pliku
        subfolder_characters: liczba początkowych znaków nazwy pliku, które tworzą opcjonalny podkatalog
    """

    def __init__(
        self,
        bucket_name: str,
        default_ext: str = None,
        subfolder_characters: int = None,
    ):
        FileStorage.__init__(
            self,
            folder_name=bucket_name,
            subfolder_characters=subfolder_characters,
            default_ext=default_ext,
        )
        self._log = logging.getLogger(__name__)

    def upload_blob(
        self, file_name: str, data: bytes, metadata: dict | BaseModel = None
    ) -> None:
        file_path = self._create_file_path(file_name)
        os.makedirs(file_path.parent, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(data)
        if metadata:
            self.put_metadata(file_name=file_name, metadata=metadata)

    def download_blob(self, file_name: str) -> bytes:
        file_path = self._create_file_path(file_name)
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def put_metadata(self, file_name: str, metadata: dict | BaseModel):
        file_path = self._create_file_path(file_name, ext="json")
        with open(file_path, "wt", encoding="utf8") as f:
            if isinstance(metadata, BaseModel):
                f.write(metadata.model_dump_json(indent=4))
            else:
                json.dump(metadata, f, indent=4, ensure_ascii=False)

    def get_metadata(self, file_name: str, clazz: BaseModel = None) -> dict | BaseModel:
        file_path = self._create_file_path(file_name, ext="json")
        try:
            with open(file_path, "rt", encoding="utf8") as f:
                d = json.load(f)
            if clazz:
                return clazz.model_validate(d)
            else:
                return d
        except FileNotFoundError:
            return None
