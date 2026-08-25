from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class BQTable(BaseYamlEntity):
    """Class representation of bigquery table iam"""

    role: Optional[str] = None
    members: Optional[list[str]] = None
    dataset_id: Optional[list[str]] = None
    table_id: Optional[list[str]] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
