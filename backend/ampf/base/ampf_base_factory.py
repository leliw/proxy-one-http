from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Type

from pydantic import BaseModel, Field

from .base_collection_storage import BaseCollectionStorage
from .base_storage import BaseStorage


class CollectionDef(BaseModel):
    """Parameters defining CollectionStorage"""
    collection_name: str
    clazz: Type
    key_name: Optional[str] = None
    subcollections: Optional[List[CollectionDef]] = Field(default_factory=lambda: [])


class AmpfBaseFactory(ABC):
    """Factory creating storage objects"""

    @abstractmethod
    def create_storage[T: BaseModel](
        self, collection_name: str, clazz: Type[T], key_name: str = None
    ) -> BaseStorage[T]:
        """Creates standard key-value storage for items of given class.

        Args:
            collection_name: name of collection where items are stored
            clazz: class of items
            key_name: name of item's property which is used as a key

        Returns:
            Storage object.
        """

    def create_compact_storage[T: BaseModel](
        self, collection_name: str, clazz: Type[T], key_name: str = None
    ) -> BaseStorage[T]:
        """Creates _compact_ key-value storage for items of given class.

        It should be used fro smaller collections.
        It creates standard storage by default.

        Args:
            collection_name: name of collection where items are stored
            clazz: class of items
            key_name: name of item's property which is used as a key

        Returns:
            Storage object.
        """
        return self.create_storage(collection_name, clazz, key_name)

    def create_collection[T](
        self, definition: CollectionDef[T] | dict
    ) -> BaseCollectionStorage[T]:
        """Creates collection from its definition. Definition can contain also subcollections definitions."""
        if isinstance(definition, dict):
            definition = CollectionDef.model_validate(dict)
        ret: BaseCollectionStorage = self.create_storage(
            definition.collection_name, definition.clazz, definition.key_name
        )
        for subcol in definition.subcollections:
            ret.add_subcollection(self.create_collection(subcol))
        return ret
