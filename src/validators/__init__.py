from src.validators.base import BaseValidator
from src.validators.bucket import BucketValidator
from src.validators.key import KeyValidator
from src.validators.keyring import KeyringValidator
from src.validators.role import RoleValidator
from src.validators.secret import SecretValidator
from src.validators.service import ServiceValidator
from src.validators.service_account import ServiceAccountValidator


def get_validator(type_: str) -> BaseValidator:
    """Returns a supported Validator class by it's type"""
    validators = {
        'bucket': BucketValidator(),
        'secret': SecretValidator(),
        'role': RoleValidator(),
        'sa': ServiceAccountValidator(),
        'service': ServiceValidator(),
        'keyring': KeyringValidator(),
        'key': KeyValidator(),
    }
    validator = validators[type_]
    return validator
