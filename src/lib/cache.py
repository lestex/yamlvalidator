from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager

import yaml

from src.lib.gcp_client import GCPClient


class Cache(ABC):
    @abstractmethod
    def load_data(self) -> None:
        pass

    @abstractmethod
    def save_data(self) -> None:
        pass

    @abstractmethod
    def get(self, smth: str) -> dict | None:
        pass

    @abstractmethod
    def put(self, smth: str) -> None:
        pass

    @abstractmethod
    def delete(self, smth: str) -> None:
        pass

    @abstractmethod
    def invalidate(self) -> None:
        pass


class FileCache(Cache):
    def __init__(self, path: str) -> None:
        """Initializes a file cache

        Args:
            path (str): File path to store cache data.
        """
        self.path = path
        self.load_data()

    def load_data(self) -> None:
        with open(self.path, 'r') as file:
            self.cache = yaml.safe_load(file)
            if not self.cache:
                self.cache = {}

    def save_data(self) -> None:
        with open(self.path, 'w') as file:
            yaml.dump(self.cache, file)

    def get(self, smth: str) -> dict | None:
        if smth in self.cache:
            return self.cache[smth]

        return None

    def put(self, smth: str) -> None:
        self.cache[smth] = {'exist': True}

    def delete(self, smth: str) -> None:
        if smth in self.cache:
            del self.cache[smth]

    def invalidate(self) -> None:
        self.cache = {}
        self.save_data()


class CacheManager:
    def __init__(
        self, cache: Cache, client: GCPClient, project: str, role: str
    ) -> None:
        self.cache = cache
        self.client = client
        self.project = project
        self.role = role

    def exists(self, group: str) -> bool:
        return self.client.group_exists(self.project, group, self.role)

    def cached(self, group: str) -> dict | None:
        return self.cache.get(group)

    def put(self, group: str) -> None:
        self.cache.put(group)

    def save(self) -> None:
        self.cache.save_data()


@contextmanager
def cache_manager(cache: Cache, client: GCPClient, project: str, role: str):
    manager = CacheManager(cache, client, project, role)
    yield manager
    manager.save()
