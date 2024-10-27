import logging
from pydantic import BaseModel
import pytest
from ampf.local.file_storage import FileStorage
from ampf.local.json_multi_files_storage import JsonMultiFilesStorage


class D1(BaseModel):
    name: str
    value: str


class D2(BaseModel):
    n: str
    v: str


@pytest.fixture
def storage(tmp_path) -> JsonMultiFilesStorage[D1]:
    FileStorage._root_dir_path = tmp_path
    return JsonMultiFilesStorage(
        path_name="test", clazz=D1, key_name="name", subfolder_characters=2
    )


def test_simple_key_all(storage):
    d = D1(name="foo", value="beer")
    storage.put("foo", d)

    assert ["foo"] == list(storage.keys())
    assert d == storage.get("foo")

    storage.delete("foo")
    assert [] == list(storage.keys())


def test_folder_key_all(storage):
    d = D1(name="foo", value="beer")
    storage.put("kung/foo", d)

    assert ["kung/foo"] == list(storage.keys())
    assert d == storage.get("kung/foo")

    storage.delete("kung/foo")
    assert [] == list(storage.keys())


@pytest.fixture
def sc_storage(storage) -> JsonMultiFilesStorage[D1]:
    logging.getLogger("ampf").setLevel(logging.DEBUG)
    storage.add_subcollection(
        JsonMultiFilesStorage(path_name="sub2", clazz=D2, key_name="n")
    )
    return storage


def test_add_and_get_subcollection(sc_storage):
    # Get subcollection by name
    sub = sc_storage.get_collection("xxx", "sub2")
    assert sub.collection_name == "test/xxx/sub2"

    # Get subcollection by class
    sub = sc_storage.get_collection("xxx", D2)
    assert sub.collection_name == "test/xxx/sub2"


def test_get_keys(sc_storage):
    # Add elements
    sc_storage.put("a", D1(name="a", value="a"))
    sc_storage.put("b", D1(name="b", value="b"))
    sub = sc_storage.get_collection("a", "sub2")
    sub.put("x", D2(n="x", v="x"))
    sub.put("y", D2(n="y", v="y"))
    sub = sc_storage.get_collection("c", "sub2")
    sub.put("z", D2(n="z", v="z"))

    # Get keys
    k = [k for k in sc_storage.keys()]

    assert len(k) == 2
    assert "a" in k
    assert "b" in k
