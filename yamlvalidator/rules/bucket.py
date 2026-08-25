from yamlvalidator.config import Config
from yamlvalidator.entities.bucket import Bucket
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules import _validate_team
from yamlvalidator.rules import _validate_unique
from yamlvalidator.rules.permissions import _validate_members_unique
from yamlvalidator.rules.permissions import _validate_permissions
from yamlvalidator.rules.permissions import _validate_permissions_members_dict


def validate_team(bucket: Bucket, config: Config) -> list[str]:
    """Validate bucket team present"""
    return _validate_team(bucket.team, config)


def validate_unique(bucket: Bucket, config: Config) -> list[str]:
    """Validates bucket is unique"""
    return _validate_unique(bucket.name, config)


def validate_fields(bucket: Bucket, config: Config) -> list[str]:
    """Validates bucket has only allowed fields"""
    fields = bucket.to_dict()
    return _validate_fields(
        bucket.class_name, bucket.valid_fields, fields, config
    )


def validate_permissions(bucket: Bucket, config: Config) -> list[str]:
    """Validate bucket has proper permissions"""
    return _validate_permissions(
        bucket.permission_types, bucket.permissions, config
    )


def validate_filename(bucket: Bucket, config: Config) -> list[str]:
    """Validates bucket created in the right file"""
    return _validate_filename(bucket.name, bucket.class_name, config)


def validate_members_unique(bucket: Bucket, config: Config) -> list[str]:
    """Validates bucket permissions members are unique"""
    return _validate_members_unique(bucket.permissions, 'permissions', config)


def validate_permissions_members(bucket: Bucket, config: Config) -> list[str]:
    """Validates bucket permissions members"""
    # we want to allow these entities for buckets
    remove_from_validation = ['allAuthenticatedUsers', 'allUsers']
    permissions = {}
    if bucket.permissions:
        for permission, members in bucket.permissions.items():
            permissions[permission] = [
                member
                for member in members
                if member not in remove_from_validation
            ]

    return _validate_permissions_members_dict(permissions, config)
