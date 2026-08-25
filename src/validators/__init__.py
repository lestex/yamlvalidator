from src.validators.base import BaseValidator
from src.validators.bucket import BucketValidator


def get_validator(type_: str) -> BaseValidator:
    """Returns a supported Validator class by it's type"""
    validators = {
        'bucket': BucketValidator(),
    }
    validator = validators[type_]
    return validator
