from dataclasses import dataclass
from typing import Optional

from src.entities.base import BaseYamlEntity


@dataclass
class Secret(BaseYamlEntity):
    """Class representation of secret YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    permissions: Optional[dict[str, list[str]]] = None

    team: Optional[str] = None
    category: Optional[str] = None
    labels: Optional[dict[str, str]] = None
    replicas: Optional[list] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def permission_types(self) -> list[str]:
        """Valid permissions type for secret defined in terraform module"""
        return [
            'secretAdmin',
            'secretAccessor',
            'secretVersionAdder',
            'secretVersionManager',
            'secretViewer',
        ]
