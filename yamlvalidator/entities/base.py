from dataclasses import dataclass
from dataclasses import fields
from typing import ClassVar
from typing import Optional


@dataclass
class BaseYamlEntity:
    """Class representation of YAML resource (entity) with common properties.
    Every entity must be a subclass of BaseYamlEntity.
    """

    # Fields that must be present and non-empty. Declared on the entity
    # so the requirement lives with the shape it describes, instead of
    # being restated as a validation function per resource type.
    required: ClassVar[tuple[str, ...]] = ()

    # Fields that may be omitted, but must not be left empty when given.
    non_empty_if_set: ClassVar[tuple[str, ...]] = ()

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
