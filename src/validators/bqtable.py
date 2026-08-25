from typing import Callable

from src.config import Config
from src.entities.base import BaseYamlEntity
from src.entities.bqtable import BQTable
from src.rules.bqtable import validate_dataset_id
from src.rules.bqtable import validate_fields
from src.rules.bqtable import validate_filename
from src.rules.bqtable import validate_members_unique
from src.rules.bqtable import validate_permissions_members
from src.rules.bqtable import validate_role
from src.rules.bqtable import validate_table_id
from src.validators.base import BaseValidator

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

    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        for _, check_func in self.checks.items():
            err = check_func(entity, config)
            if err:
                self.errors.extend(err)
