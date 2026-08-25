from typing import Callable

from src.config import Config
from src.entities.secret import Secret
from src.rules.secret import validate_category
from src.rules.secret import validate_fields
from src.rules.secret import validate_filename
from src.rules.secret import validate_labels
from src.rules.secret import validate_members_unique
from src.rules.secret import validate_name
from src.rules.secret import validate_permissions
from src.rules.secret import validate_permissions_members
from src.rules.secret import validate_team
from src.rules.secret import validate_unique
from src.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains secret entity
checks: dict[str, Callable[[Secret, Config], list[str]]] = {
    'validate_name': validate_name,
    'validate_team': validate_team,
    'validate_category': validate_category,
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
