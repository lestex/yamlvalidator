from typing import Callable

from src.config import Config
from src.entities.base import BaseYamlEntity
from src.entities.key import Key
from src.rules.key import validate_fields
from src.rules.key import validate_filename
from src.rules.key import validate_is_version_template
from src.rules.key import validate_key_purpose
from src.rules.key import validate_key_rotation_period
from src.rules.key import validate_keyring_name
from src.rules.key import validate_members_unique
from src.rules.key import validate_name
from src.rules.key import validate_permissions_members
from src.rules.key import validate_unique
from src.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains entity
checks: dict[str, Callable[[Key, Config], list[str]]] = {
    'validate_name': validate_name,
    'validate_unique': validate_unique,
    'validate_filename': validate_filename,
    'validate_fields': validate_fields,
    'validate_is_version_template': validate_is_version_template,
    'validate_keyring_name': validate_keyring_name,
    'validate_key_rotation_period': validate_key_rotation_period,
    'validate_members_unique': validate_members_unique,
    'validate_permissions_members': validate_permissions_members,
    'validate_key_purpose': validate_key_purpose,
}


class KeyValidator(BaseValidator):
    """Keyring validator class"""

    checks: dict = checks.copy()

    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        for _, check_func in self.checks.items():
            err = check_func(entity, config)
            if err:
                self.errors.extend(err)
