from yamlvalidator.config import Config
from yamlvalidator.entities.role import Role
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules import _validate_unique
from yamlvalidator.rules.permissions import _validate_members_unique
from yamlvalidator.rules.permissions import _validate_permissions_members_list


def validate_role(role: Role, config: Config) -> list[str]:
    """Validates role name properly set"""
    errors = []

    if role.role:
        role_name = role.role.split('/')
        if 'roles' not in role_name:
            errors.append(
                f"{role.class_name!r} might be incorrect, must include 'roles/'"  # noqa E501
            )
    return errors


def validate_fields(role: Role, config: Config) -> list[str]:
    """Validates role has only allowed fields"""
    fields = role.to_dict()
    return _validate_fields(role.class_name, role.valid_fields, fields, config)


def validate_unique(role: Role, config: Config) -> list[str]:
    """Validates role is unique"""
    return _validate_unique(role.role, config)


def validate_filename(role: Role, config: Config) -> list[str]:
    """Validates role name present in the filename"""
    errors = []

    if role.role:
        role_name = role.role.split('/')[-1].replace('.', '_')
        errors.extend(_validate_filename(role_name, role.class_name, config))
    return errors


def validate_members_unique(role: Role, config: Config) -> list[str]:
    """Validates role permissions members are unique"""
    return _validate_members_unique(role.members, 'members', config)


def validate_permissions_members(role: Role, config: Config) -> list[str]:
    """Validates bucket permissions members"""
    return _validate_permissions_members_list('members', role.members, config)
