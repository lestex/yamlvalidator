from abc import ABC
from abc import abstractmethod
from typing import Callable

from src.config import Config
from src.entities.base import BaseYamlEntity

Check = Callable[[BaseYamlEntity, Config], list[str]]


class BaseValidator(ABC):
    """Abstract validator class, must not be instantiated directly.

    A subclass only declares `checks`; running them is the same for
    every resource type.
    """

    # a subclass satisfies this with its own dict of rules, which is
    # what keeps the base class itself abstract
    @property
    @abstractmethod
    def checks(self) -> dict[str, Check]:
        """The rules this validator runs, in order."""

    def __init__(self) -> None:
        # per instance: a class attribute would be shared by every
        # validator subclass
        self.errors: list[str] = []

    def clear(self) -> None:
        """Clears errors for validator"""
        self.errors.clear()

    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        """Runs validate functions against entity object"""
        for _, check_func in self.checks.items():
            err = check_func(entity, config)
            if err:
                self.errors.extend(err)
