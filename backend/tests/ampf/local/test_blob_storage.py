import json
import pytest
from pydantic import BaseModel, Field

from ampf.local.blob_storage import LocalBlobStorage
from ampf.local.file_storage import FileStorage


class MyMetadata(BaseModel):
    name: str = Field(...)
    age: int = Field(...)


@pytest.fixture
def storage(tmp_path):
    FileStorage._root_dir_path = tmp_path
    return LocalBlobStorage("test_bucket", subfolder_characters=2)


def test_upload_blob(tmp_path, storage):
    file_name = "test/file.txt"
    data = b"test data"
    storage.upload_blob(file_name, data)
    exp_path = tmp_path.joinpath("test_bucket", "test", "fi", "file.txt")
    assert exp_path.exists()
    with open(exp_path, "rb") as f:
        assert f.read() == data


def test_upload_blob_with_metadata(tmp_path, storage):
    file_name = "test/file.txt"
    data = b"test data"
    metadata = {"name": "test", "age": 10}
    storage.upload_blob(file_name, data, metadata)
    exp_path = tmp_path.joinpath("test_bucket", "test", "fi", "file.txt.json")
    assert exp_path.exists()
    with open(exp_path, "rt", encoding="utf8") as f:
        assert json.load(f) == metadata


def test_upload_blob_with_pydantic_metadata(tmp_path, storage):
    file_name = "test/file.txt"
    data = b"test data"
    metadata = MyMetadata(name="test", age=10)
    storage.upload_blob(file_name, data, metadata)
    exp_path = tmp_path.joinpath("test_bucket", "test", "fi", "file.txt.json")
    assert exp_path.exists()
    with open(exp_path, "rt", encoding="utf8") as f:
        assert json.load(f) == {"name": "test", "age": 10}


def test_download_blob(storage):
    file_name = "test/file.txt"
    data = b"test data"
    storage.upload_blob(file_name, data)
    downloaded_data = storage.download_blob(file_name)
    assert downloaded_data == data


def test_download_nonexistent_blob(storage):
    file_name = "test/file.txt"
    downloaded_data = storage.download_blob(file_name)
    assert downloaded_data is None


def test_get_metadata(storage):
    file_name = "test/file.txt"
    metadata = {"name": "test", "age": 10}
    storage.upload_blob(file_name, b"test data", metadata)
    retrieved_metadata = storage.get_metadata(file_name)
    assert retrieved_metadata == metadata


def test_get_metadata_with_class(storage):
    file_name = "test/file.txt"
    metadata = MyMetadata(name="test", age=10)
    storage.upload_blob(file_name, b"test data", metadata)
    retrieved_metadata = storage.get_metadata(file_name, clazz=MyMetadata)
    assert retrieved_metadata == metadata


def test_get_nonexistent_metadata(storage):
    file_name = "test/file.txt"
    retrieved_metadata = storage.get_metadata(file_name)
    assert retrieved_metadata is None


def test_upload_blob_with_default_ext(tmp_path, storage):
    storage = LocalBlobStorage(str(tmp_path.joinpath("test_bucket")), default_ext="txt", subfolder_characters=2)
    file_name = "test/file"
    data = b"test data"
    storage.upload_blob(file_name, data)
    exp_path = tmp_path.joinpath("test_bucket", "test", "fi", "file.txt")
    assert exp_path.exists()
    with open(exp_path, "rb") as f:
        assert f.read() == data
