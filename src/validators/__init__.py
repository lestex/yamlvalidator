from src.validators.base import BaseValidator
from src.validators.bucket import BucketValidator
from src.validators.secret import SecretValidator


def get_validator(type_: str) -> BaseValidator:
    """Returns a supported Validator class by it's type"""
    validators = {
        'bucket': BucketValidator(),
        'secret': SecretValidator(),
    }
    validator = validators[type_]
    return validator
