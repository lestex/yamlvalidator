from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.bqdataset import BQDataset
from yamlvalidator.rules import validate_required
from yamlvalidator.rules.bqdataset import validate_fields
from yamlvalidator.rules.bqdataset import validate_filename
from yamlvalidator.rules.bqdataset import validate_members_unique
from yamlvalidator.rules.bqdataset import validate_permissions_members
from yamlvalidator.rules.bqdataset import validate_role
from yamlvalidator.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains role entity
checks: dict[str, Callable[[BQDataset, Config], list[str]]] = {
    'validate_role': validate_role,
    'validate_required': validate_required,
    'validate_fields': validate_fields,
    'validate_filename': validate_filename,
    'validate_members_unique': validate_members_unique,
    'validate_permissions_members': validate_permissions_members,
}


class BQDatasetValidator(BaseValidator):
    """BQDataset validator class"""

    checks: dict = checks.copy()
