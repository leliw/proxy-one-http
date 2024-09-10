from pydantic import BaseModel

from ampf.storage_in_memory import AmpfInMemoryFactory, InMemoryStorage


class D(BaseModel):
    name: str
    value: str


def test_storage_all():
    t = InMemoryStorage(D)
    d = D(name="foo", value="beer")
    t.put("foo", d)

    assert ["foo"] == list(t.keys())
    assert d == t.get("foo")

    t.delete("foo")
    assert [] == list(t.keys())
    assert t.get("foo") is None

def test_storage_factory():
    t1 = AmpfInMemoryFactory()
    s1 = t1.create_storage("xxx", D)
    s1.save(D(name="1", value="a"))

    t2 = AmpfInMemoryFactory()
    s2 = t2.create_storage("xxx", D)

    assert list(s2.keys()) == ["1"]