from __future__ import annotations
from typing import List, Type
from pydantic import BaseModel

from .base_storage import BaseStorage


class BaseCollectionStorage[T](BaseStorage[T]):
    """Base class for stored collections.
    Each element of collection can have its own subcollections
    """

    def __init__(
        self,
        collection_name: str,
        clazz: Type[T],
        key_name: str = None,
        subcollections: List[BaseCollectionStorage] = None,
    ):
        super().__init__(clazz=clazz, key_name=key_name)
        self.collection_name = collection_name
        self.subcollections: dict[str, BaseCollectionStorage] = {}
        self.sub_classes: dict[Type, str] = {}
        if subcollections:
            for sc in subcollections:
                self.add_subcollection(sc)

    def add_subcollection[Y: BaseModel](self, subcollection: BaseCollectionStorage[Y]):
        """Adds subcollection definition

        Args:
            subcollection (BaseCollectionStorage[Y]): subcollectiondefinition
        """
        self.subcollections[subcollection.collection_name] = subcollection
        self.sub_classes[subcollection.clazz] = subcollection.collection_name

    def get_collection[Y: BaseModel](
        self, key: str, subcollection_name_or_class: str | Type[Y]
    ) -> BaseCollectionStorage[Y]:
        """Returns subcollection for given key.

        Subcollection can be identified by its name or class.

        Args:
            key (str): Main collection key
            subcollection_name_or_class (str | Type[Y]): Subcollection name or its class
        Returns:
            (BaseCollectionStorage[Y]): Subcollection object
        """
        if not isinstance(subcollection_name_or_class, str):
            subcollection_name = self.sub_classes[subcollection_name_or_class]
        else:
            subcollection_name = subcollection_name_or_class
        sub = self.subcollections[subcollection_name]
        ret = sub.__class__(
            f"{self.collection_name}/{key}/{sub.collection_name}",
            clazz=sub.clazz,
            key_name=sub.key_name,
        )
        for c in sub.subcollections.values():
            ret.add_subcollection(c)
        return ret
