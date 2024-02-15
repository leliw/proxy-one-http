"""Siple file based storage"""
import logging
from .basic_storage import BasicStorage


class KeyNotExists(Exception):
    """Raised when key is not found"""

class Storage(BasicStorage):
    """Stores data on disk (key: value)"""
    def __init__(self, base_path="data"):
        super().__init__(base_path)
        self._log = logging.getLogger(__name__)
