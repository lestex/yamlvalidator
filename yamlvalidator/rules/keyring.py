from yamlvalidator.config import Config
from yamlvalidator.entities.keyring import Keyring
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules import _validate_unique


def validate_unique(keyring: Keyring, config: Config) -> list[str]:
    """Validates keyring is unique"""
    return _validate_unique(keyring.name, config)


def validate_fields(keyring: Keyring, config: Config) -> list[str]:
    """Validates keyring has only allowed fields"""
    fields = keyring.to_dict()
    return _validate_fields(
        keyring.class_name, keyring.valid_fields, fields, config
    )


def validate_filename(keyring: Keyring, config: Config) -> list[str]:
    """Validates keyring created in the right file"""
    return _validate_filename(keyring.name, keyring.class_name, config)
