from typing import Callable

from src.config import Config
from src.entities.base import BaseYamlEntity
from src.entities.keyring import Keyring
from src.rules.keyring import validate_fields
from src.rules.keyring import validate_filename
from src.rules.keyring import validate_name
from src.rules.keyring import validate_unique
from src.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains entity
checks: dict[str, Callable[[Keyring, Config], list[str]]] = {
    'validate_name': validate_name,
    'validate_unique': validate_unique,
    'validate_filename': validate_filename,
    'validate_fields': validate_fields,
}


class KeyringValidator(BaseValidator):
    """Keyring validator class"""

    checks: dict = checks.copy()

    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        for _, check_func in self.checks.items():
            err = check_func(entity, config)
            if err:
                self.errors.extend(err)
