from typing import Callable

from yamlvalidator.config import Config
from yamlvalidator.entities.bucket import Bucket
from yamlvalidator.rules.bucket import validate_fields
from yamlvalidator.rules.bucket import validate_filename
from yamlvalidator.rules.bucket import validate_members_unique
from yamlvalidator.rules.bucket import validate_name
from yamlvalidator.rules.bucket import validate_permissions
from yamlvalidator.rules.bucket import validate_permissions_members
from yamlvalidator.rules.bucket import validate_team
from yamlvalidator.rules.bucket import validate_unique
from yamlvalidator.validators.base import BaseValidator

# a dictionary holds all validation functions to be run agains bucket entity
checks: dict[str, Callable[[Bucket, Config], list[str]]] = {
    'validate_name': validate_name,
    'validate_team': validate_team,
    'validate_unique': validate_unique,
    'validate_members_unique': validate_members_unique,
    'validate_filename': validate_filename,
    'validate_permissions': validate_permissions,
    'validate_permissions_members': validate_permissions_members,
    'validate_fields': validate_fields,
}


class BucketValidator(BaseValidator):
    """Buckets validator class"""

    checks: dict = checks.copy()
