from typing import Callable

from src.config import Config
from src.entities.base import BaseYamlEntity
from src.entities.bucket import Bucket
from src.rules.bucket import validate_fields
from src.rules.bucket import validate_filename
from src.rules.bucket import validate_members_unique
from src.rules.bucket import validate_name
from src.rules.bucket import validate_permissions
from src.rules.bucket import validate_permissions_members
from src.rules.bucket import validate_team
from src.rules.bucket import validate_unique
from src.validators.base import BaseValidator

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

    def validate(self, entity: BaseYamlEntity, config: Config) -> None:
        for _, check_func in self.checks.items():
            err = check_func(entity, config)
            if err:
                self.errors.extend(err)
