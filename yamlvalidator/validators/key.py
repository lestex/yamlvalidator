from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.key import Key
from yamlvalidator.rules import validate_required
from yamlvalidator.rules.key import validate_fields
from yamlvalidator.rules.key import validate_filename
from yamlvalidator.rules.key import validate_is_version_template
from yamlvalidator.rules.key import validate_key_purpose
from yamlvalidator.rules.key import validate_key_rotation_period
from yamlvalidator.rules.key import validate_members_unique
from yamlvalidator.rules.key import validate_permissions_members
from yamlvalidator.rules.key import validate_unique
from yamlvalidator.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains entity
checks: dict[str, Callable[[Key, Config], list[str]]] = {
    'validate_required': validate_required,
    'validate_unique': validate_unique,
    'validate_filename': validate_filename,
    'validate_fields': validate_fields,
    'validate_is_version_template': validate_is_version_template,
    'validate_key_rotation_period': validate_key_rotation_period,
    'validate_members_unique': validate_members_unique,
    'validate_permissions_members': validate_permissions_members,
    'validate_key_purpose': validate_key_purpose,
}


class KeyValidator(BaseValidator):
    """Keyring validator class"""

    checks: dict = checks.copy()
