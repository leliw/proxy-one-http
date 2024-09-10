"""In memory storage implemenation - for tests"""
from typing import Iterator, Type
from pydantic import BaseModel
from .base.ampf_base_factory import AmpfBaseFactory
from .base.base_storage import BaseStorage


class InMemoryStorage[T: BaseModel](BaseStorage):
    def __init__(self, clazz: Type[T], key_name: str = None):
        super().__init__(clazz, key_name)
        self.items = {}

    def put(self, key: str, value: T) -> None:
        self.items[key] = value

    def get(self, key: str) -> T:
        return self.items.get(key)

    def keys(self) -> Iterator[T]:
        return self.items.keys()

    def delete(self, key: str) -> None:
        self.items.pop(key, None)


class AmpfInMemoryFactory(AmpfBaseFactory):
    collections = {}

    def create_storage[T: BaseModel](
        self, collection_name: str, clazz: Type[T], key_name: str = None
    ) -> BaseStorage[T]:
        if collection_name not in self.collections:
            self.collections[collection_name] = InMemoryStorage(
                clazz=clazz, key_name=key_name
            )
        return self.collections.get(collection_name)
