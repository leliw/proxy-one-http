"""Base class for storage implementations which store Pydantic objects"""

from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Callable, Generator, Iterator, Type, TypeVar

T = TypeVar("T", bound=BaseModel)


class KeyException(Exception):
    def __init__(self, collection_name: str = None, clazz: Type = None, key: str = None):
        self.collection_name = collection_name
        self.clazz= clazz
        self.key = key


class KeyNotExists(KeyException):
    def __init__(self, collection_name: str = None, clazz: Type = None, key: str = None):
        super().__init__(collection_name, clazz, key)


class KeyExists(KeyException):
    def __init__(self, collection_name: str = None, clazz: Type = None, key: str = None):
        super().__init__(collection_name, clazz, key)


class Query[T]:
    def __init__(self, src: Callable[[], Generator[T]]):
        self._src = src

    def where(self, field: str, op: str, value: str) -> Query[T]:
        def it():
            return (o for o in self._src() if o.__getattribute__(field) == value)

        return Query(it)

    def get_all(self) -> Generator[T]:
        return self._src()


class BaseStorage[T](ABC, Query[T]):
    """Base class for storage implementations which store Pydantic objects

    Parameters:
    ----------
    clazz: Type[T]
        The Pydantic class to store
    key_name: str
        The key name to use for the storage. If not specified first field is taken
    """

    def __init__(self, clazz: Type[T], key_name: str = None):
        self.clazz = clazz
        if not key_name:
            field_names = list(clazz.model_fields.keys())
            key_name = field_names[0]
        self.key_name = key_name
        Query.__init__(self, self.get_all)

    @abstractmethod
    def put(self, key: str, value: T) -> None:
        """Store the value with the key"""

    @abstractmethod
    def get(self, key: str) -> T:
        """Get the value with the key"""

    @abstractmethod
    def keys(self) -> Iterator[T]:
        """Get all the keys"""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete the value with the key"""

    def create(self, value: T) -> None:
        """Adds to collection a new element but only if such key doesn't already exists"""
        key = self.get_key(value)
        if self.key_exists(key):
            raise KeyExists
        self.put(key, value)

    def save(self, value: T) -> None:
        key = self.get_key(value)
        self.put(key, value)

    def get_key(self, value: T) -> str:
        return getattr(value, self.key_name)

    def drop(self) -> None:
        """Delete all the values"""
        for key in self.keys():
            self.delete(key)

    def get_all(self) -> Iterator[T]:
        """Get all the values"""
        for key in self.keys():
            yield self.get(key)

    def key_exists(self, needle: str) -> bool:
        for key in self.keys():
            if needle == key:
                return True
        return False

    def is_empty(self) -> bool:
        """Is storage empty?"""
        for _ in self.keys():
            return False
        return True
