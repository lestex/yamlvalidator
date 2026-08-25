from yamlvalidator.config import Config
from yamlvalidator.entities.secret import Secret
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules import _validate_labels
from yamlvalidator.rules import _validate_team
from yamlvalidator.rules import _validate_unique
from yamlvalidator.rules.permissions import _validate_members_unique
from yamlvalidator.rules.permissions import _validate_permissions
from yamlvalidator.rules.permissions import _validate_permissions_members_dict


def validate_team(secret: Secret, config: Config) -> list[str]:
    """Validate secret team present"""
    return _validate_team(secret.team, config)


def validate_unique(secret: Secret, config: Config) -> list[str]:
    """Validates secret is unique"""
    return _validate_unique(secret.name, config)


def validate_fields(secret: Secret, config: Config) -> list[str]:
    """Validates secret has only allowed fields"""
    fields = secret.to_dict()
    return _validate_fields(
        secret.class_name, secret.valid_fields, fields, config
    )


def validate_permissions(secret: Secret, config: Config) -> list[str]:
    """Validate secret has proper permissions"""
    return _validate_permissions(
        secret.permission_types, secret.permissions, config
    )


def validate_filename(secret: Secret, config: Config) -> list[str]:
    """Validates secret created in the right file"""
    return _validate_filename(secret.name, secret.class_name, config)


def validate_labels(secret: Secret, config: Config) -> list[str]:
    """Validates secret has labels"""
    return _validate_labels(secret.labels, config)


def validate_members_unique(secret: Secret, config: Config) -> list[str]:
    """Validates secret permissions members are unique"""
    return _validate_members_unique(secret.permissions, 'permissions', config)


def validate_permissions_members(secret: Secret, config: Config) -> list[str]:
    """Validates secret permissions members"""
    return _validate_permissions_members_dict(secret.permissions, config)
