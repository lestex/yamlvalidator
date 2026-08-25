from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class Role(BaseYamlEntity):
    """Class representation of role YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    role: Optional[str] = None
    members: Optional[list[str]] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
