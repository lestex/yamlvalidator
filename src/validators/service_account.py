from typing import Callable

from src.config import Config
from src.entities.base import BaseYamlEntity
from src.entities.service_account import ServiceAccount
from src.rules.service_account import validate_description
from src.rules.service_account import validate_disabled
from src.rules.service_account import validate_display_name
from src.rules.service_account import validate_fields
from src.rules.service_account import validate_filename
from src.rules.service_account import validate_members_unique
from src.rules.service_account import validate_permissions_members
from src.rules.service_account import validate_service_account_id
from src.rules.service_account import validate_unique
from src.validators.base import BaseValidator

# a dictionary holds all validation functions to be run
checks: dict[str, Callable[[ServiceAccount, Config], list[str]]] = {
    'validate_service_account_id': validate_service_account_id,
    'validate_fields': validate_fields,
    'validate_unique': validate_unique,
    'validate_members_unique': validate_members_unique,
    'validate_filename': validate_filename,
    'validate_description': validate_description,
    'validate_display_name': validate_display_name,
    'validate_disabled': validate_disabled,
    'validate_permissions_members': validate_permissions_members,
}


class ServiceAccountValidator(BaseValidator):
    """ServiceAccount validator class"""

    checks: dict = checks.copy()

    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        for _, check_func in self.checks.items():
            err = check_func(entity, config)
            if err:
                self.errors.extend(err)
