from abc import ABC
from abc import abstractmethod

from src.config import Config
from src.entities.base import BaseYamlEntity


class BaseValidator(ABC):
    """Abstract validator class, must not be instantiated directly"""

    def __init__(self) -> None:
        # per instance: a class attribute would be shared by every
        # validator subclass
        self.errors: list[str] = []

    def clear(self) -> None:
        """Clears errors for validator"""
        self.errors.clear()

    @abstractmethod
    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        """Runs validate functions against entity object"""
        pass
