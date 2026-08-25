from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.service_account import ServiceAccount
from yamlvalidator.rules.service_account import validate_description
from yamlvalidator.rules.service_account import validate_disabled
from yamlvalidator.rules.service_account import validate_display_name
from yamlvalidator.rules.service_account import validate_fields
from yamlvalidator.rules.service_account import validate_filename
from yamlvalidator.rules.service_account import validate_members_unique
from yamlvalidator.rules.service_account import validate_permissions_members
from yamlvalidator.rules.service_account import validate_service_account_id
from yamlvalidator.rules.service_account import validate_unique
from yamlvalidator.validators.base import BaseValidator

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
