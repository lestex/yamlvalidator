from dataclasses import dataclass

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class Keyring(BaseYamlEntity):
    """Class representation of keyring YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
