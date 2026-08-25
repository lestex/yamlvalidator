from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.secret import Secret
from yamlvalidator.rules import validate_required
from yamlvalidator.rules.secret import validate_fields
from yamlvalidator.rules.secret import validate_filename
from yamlvalidator.rules.secret import validate_labels
from yamlvalidator.rules.secret import validate_members_unique
from yamlvalidator.rules.secret import validate_permissions
from yamlvalidator.rules.secret import validate_permissions_members
from yamlvalidator.rules.secret import validate_team
from yamlvalidator.rules.secret import validate_unique
from yamlvalidator.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains secret entity
checks: dict[str, Callable[[Secret, Config], list[str]]] = {
    'validate_required': validate_required,
    'validate_team': validate_team,
    'validate_labels': validate_labels,
    'validate_unique': validate_unique,
    'validate_members_unique': validate_members_unique,
    'validate_filename': validate_filename,
    'validate_permissions': validate_permissions,
    'validate_permissions_members': validate_permissions_members,
    'validate_fields': validate_fields,
}


class SecretValidator(BaseValidator):
    """Secrets validator class"""

    checks: dict = checks.copy()
