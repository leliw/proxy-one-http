from pydantic import BaseModel
import pytest
from ampf.local.file_storage import FileStorage
from ampf.local.json_multi_files_storage import JsonMultiFilesStorage


class D(BaseModel):
    name: str
    value: str


@pytest.fixture
def storage(tmp_path):
    FileStorage._root_dir_path = tmp_path
    return JsonMultiFilesStorage[D](
        path_name="test", clazz=D, key_name="name", subfolder_characters=2
    )


def test_simple_key_all(storage):
    d = D(name="foo", value="beer")
    storage.put("foo", d)

    assert ["foo"] == list(storage.keys())
    assert d == storage.get("foo")

    storage.delete("foo")
    assert [] == list(storage.keys())
    assert storage.get("foo") is None


def test_folder_key_all(storage):
    d = D(name="foo", value="beer")
    storage.put("kung/foo", d)

    assert ["kung/foo"] == list(storage.keys())
    assert d == storage.get("kung/foo")

    storage.delete("kung/foo")
    assert [] == list(storage.keys())
    assert storage.get("kung/foo") is None
