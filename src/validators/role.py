from typing import Callable

from src.config import Config
from src.entities.role import Role
from src.rules.role import validate_fields
from src.rules.role import validate_filename
from src.rules.role import validate_members_unique
from src.rules.role import validate_permissions_members
from src.rules.role import validate_role
from src.rules.role import validate_unique
from src.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains role entity
checks: dict[str, Callable[[Role, Config], list[str]]] = {
    'validate_role': validate_role,
    'validate_fields': validate_fields,
    'validate_role_unique': validate_unique,
    'validate_filename': validate_filename,
    'validate_members_unique': validate_members_unique,
    'validate_permissions_members': validate_permissions_members,
}


class RoleValidator(BaseValidator):
    """Role validator class"""

    checks: dict = checks.copy()
