from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.keyring import Keyring
from yamlvalidator.rules import validate_required
from yamlvalidator.rules.keyring import validate_fields
from yamlvalidator.rules.keyring import validate_filename
from yamlvalidator.rules.keyring import validate_unique
from yamlvalidator.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains entity
checks: dict[str, Callable[[Keyring, Config], list[str]]] = {
    'validate_required': validate_required,
    'validate_unique': validate_unique,
    'validate_filename': validate_filename,
    'validate_fields': validate_fields,
}


class KeyringValidator(BaseValidator):
    """Keyring validator class"""

    checks: dict = checks.copy()
