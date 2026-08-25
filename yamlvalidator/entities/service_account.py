from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class ServiceAccount(BaseYamlEntity):
    """Class representation of service_account YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    non_empty_if_set = ('description', 'display_name')

    account_id: Optional[str] = None
    disabled: Optional[bool] = None
    display_name: Optional[str] = None
    description: Optional[str] = None

    serviceAccountUser: Optional[list[str]] = None
    workloadIdentityUser: Optional[list[str]] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def class_name(self) -> str:
        """explicitly return `sa` since we use it in filenames"""
        return 'sa'
