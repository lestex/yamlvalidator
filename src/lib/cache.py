from abc import ABC
from abc import abstractmethod

import yaml


class Cache(ABC):
    @abstractmethod
    def load_data(self) -> None:
        pass

    @abstractmethod
    def get(self, smth: str) -> dict | None:
        pass


class FileCache(Cache):
    """A read-only view of the group membership cache.

    The tool never writes to this file: it is populated out-of-band
    (see README) and read here to answer "does this group exist?".
    """

    def __init__(self, path: str) -> None:
        """Initializes a file cache

        Args:
            path (str): File path the cache data is read from.
        """
        self.path = path
        self.load_data()

    def load_data(self) -> None:
        with open(self.path, 'r') as file:
            self.cache = yaml.safe_load(file)
            if not self.cache:
                self.cache = {}

    def get(self, smth: str) -> dict | None:
        if smth in self.cache:
            return self.cache[smth]

        return None
