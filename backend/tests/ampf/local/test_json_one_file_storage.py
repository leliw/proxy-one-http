from pydantic import BaseModel
import pytest
from ampf.base.base_storage import KeyExists
from ampf.local.file_storage import FileStorage
from ampf.local.json_one_file_storage import JsonOneFileStorage


class D(BaseModel):
    name: str
    value: str

@pytest.fixture
def t(tmp_path):
    FileStorage._root_dir_path = tmp_path
    return JsonOneFileStorage[D]("data", D)


def test_constructor(tmp_path):
    # Basic usage - file_name as string
    FileStorage._root_dir_path = tmp_path
    t = JsonOneFileStorage[D](file_name="data", clazz=D, key_name="name")
    assert t.file_path == tmp_path.joinpath("data.json")
    # Basic usage - subcollections
    t = JsonOneFileStorage[D]("users/user_id/preferences", D, key_name="name")
    assert t.file_path == tmp_path.joinpath("users/user_id/preferences.json")
    # test file name - string with ext
    t3 = JsonOneFileStorage[D]("data.json", D, key_name="name")
    assert t3.file_path == tmp_path.joinpath("data.json")
    # test file name - string without ext
    t4 = JsonOneFileStorage[D]("data", D, key_name="name")
    assert t4.file_path == tmp_path.joinpath("data.json")


def test_simple_key_all(t):
    d = D(name="foo", value="beer")
    t.put("foo", d)

    assert ["foo"] == list(t.keys())
    assert d == t.get("foo")

    t.delete("foo")
    assert [] == list(t.keys())
    assert t.get("foo") is None


def test_folder_key_all(t):
    d = D(name="kung/foo", value="beer")
    t.put("kung/foo", d)

    assert ["kung/foo"] == list(t.keys())
    assert d == t.get("kung/foo")

    t.delete("kung/foo")
    assert [] == list(t.keys())
    assert t.get("kung/foo") is None

def test_is_empty(t):
    assert t.is_empty()

def test_create(t):
    d = D(name="foo", value="beer")
    t.create(d)
    assert ["foo"] == list(t.keys())
    with pytest.raises(KeyExists):
        t.create(d)
    
def test_drop(t):
    d = D(name="foo", value="beer")
    t.create(d)

    t.drop()

    assert t.is_empty()


def test_where(t):
    t.save(D(name="1", value="a"))
    t.save(D(name="2", value="b"))
    t.save(D(name="3", value="b"))

    l1 = list(t.where("value", "==", "b").get_all())
    assert 2 == len(l1)

    l2 = list(t.where("value", "==", "b").get_all())
    assert 2 == len(l2)


def test_key_isnt_stored_in_value(t):
    t.save(D(name="1", value="a"))
    d = t._load_data()

    assert "1" in d.keys()
    assert "name" not in d["1"].keys()
