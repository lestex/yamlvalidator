from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class BQDataset(BaseYamlEntity):
    """Class representation of bigquery dataset iam"""

    role: Optional[str] = None
    members: Optional[list[str]] = None
    dataset_id: Optional[list[str]] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
