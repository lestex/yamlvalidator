from dataclasses import dataclass
from dataclasses import fields
from typing import Optional


@dataclass
class BaseYamlEntity:
    """Class representation of YAML resource (entity) with common properties.
    Every entity must be a subclass of BaseYamlEntity.
    """

    # Every YAML resource has name.
    name: Optional[str] = None

    @property
    def valid_fields(self) -> list[str]:
        """Class properties we can validate"""
        return [field.name for field in fields(self)]

    @property
    def class_name(self) -> str:
        """Returns a class name"""
        cls_name = type(self).__name__
        return cls_name.lower()

    def to_dict(self):
        return self.__dict__
