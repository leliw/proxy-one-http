from abc import ABC
import os
from pathlib import Path

type StrPath = str | Path


class FileStorage(ABC):
    """Klasa bazowa dla magazynów operujących na plikach lokalnych.

    W celu poprawy wydajności operacji na plikach, mogą być tworzone dodatkowe podkatalogi.

    Atrybut klasy `_root_dir_path` określa katalog główny wszystkich danych zapisywanych na
    dysku przez klasy dziedziczące.

    Args:
        folder_name: katalog w którym są składowane pliki
        default_ext: domyślne rozszerzenie plików
        subfolder_characters: liczba początkowych znaków, które tworzą opcjonalny podkatalog
    """

    _root_dir_path = Path("data")

    def __init__(
        self,
        folder_name: str = None,
        default_ext: str = None,
        subfolder_characters: int = None,
    ):
        if folder_name:
            self.folder_path = self._root_dir_path.joinpath(folder_name)
        else:
            self.folder_path = self._root_dir_path
        self.subfolder_characters = subfolder_characters
        self.default_ext = default_ext
        os.makedirs(self.folder_path, exist_ok=True)

    def _split_to_folders(self, file_name: str) -> list[str]:
        """Adds extra subfolder if subfolder_characters is set"""
        folders = file_name.split("/")
        if self.subfolder_characters:
            file_name = folders.pop()
            sub_folder = file_name[0 : self.subfolder_characters]
            return [*folders, sub_folder, file_name]
        else:
            return folders

    def _create_file_path(self, file_name: str, ext: str = None) -> Path:
        ext = ext or self.default_ext
        if ext:
            file_name = f"{file_name}.{ext}"
        path = self.folder_path.joinpath(*self._split_to_folders(file_name))
        os.makedirs(path.parent, exist_ok=True)
        return path
