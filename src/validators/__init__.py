from src.validators.base import BaseValidator


def get_validator(type_: str) -> BaseValidator:
    """Returns a supported Validator class by it's type"""
    validators: dict[str, BaseValidator] = {}
    validator = validators[type_]
    return validator
