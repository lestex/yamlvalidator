from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.bqtable import BQTable
from yamlvalidator.rules.bqtable import validate_dataset_id
from yamlvalidator.rules.bqtable import validate_fields
from yamlvalidator.rules.bqtable import validate_filename
from yamlvalidator.rules.bqtable import validate_members_unique
from yamlvalidator.rules.bqtable import validate_permissions_members
from yamlvalidator.rules.bqtable import validate_role
from yamlvalidator.rules.bqtable import validate_table_id
from yamlvalidator.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains role entity
checks: dict[str, Callable[[BQTable, Config], list[str]]] = {
    'validate_role': validate_role,
    'validate_dataset_id': validate_dataset_id,
    'validate_table_id': validate_table_id,
    'validate_fields': validate_fields,
    'validate_filename': validate_filename,
    'validate_members_unique': validate_members_unique,
    'validate_permissions_members': validate_permissions_members,
}


class BQTableValidator(BaseValidator):
    """BQTable validator class"""

    checks: dict = checks.copy()
