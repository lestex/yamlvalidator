from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class Service(BaseYamlEntity):
    """Class representation of service YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    required = ('service',)

    service: Optional[str] = None
    disable_on_destroy: Optional[bool] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
