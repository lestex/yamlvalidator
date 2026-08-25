from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class Bucket(BaseYamlEntity):
    """Class representation of bucket YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    required = ('name', 'team')

    permissions: Optional[dict[str, list[str]]] = None

    team: Optional[str] = None
    bucket_name: Optional[str] = None
    cors: Optional[dict] = None
    default_kms_key_name: Optional[str] = None
    folders: Optional[list[str]] = None
    force_destroy: Optional[bool] = None
    hmac_service_accounts: Optional[dict] = None
    labels: Optional[dict[str, str]] = None
    lifecycle_rules: Optional[list[str]] = None
    location: Optional[str] = None
    log_bucket: Optional[str] = None
    log_object_prefix: Optional[str] = None
    notification_event_types: Optional[str] = None
    notification_payload: Optional[str] = None
    notification_object_name_prefix: Optional[str] = None
    requester_pays: Optional[bool] = None
    retention_policy: Optional[dict] = None
    storage_class: Optional[str] = None
    storage_class_backup: Optional[str] = None
    topic: Optional[str] = None
    topic_serviceaccount: Optional[list[str]] = None
    uniform_bucket_level_access: Optional[bool] = None
    versioning: Optional[bool] = None
    website: Optional[dict] = None
    description: Optional[str] = None
    enable_backup_bucket: Optional[bool] = None
    schedule: Optional[list[str]] = None
    transfer_spec: Optional[list[str]] = None
    autoclass_enable: Optional[bool] = None
    terminal_storage_class: Optional[str] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def permission_types(self) -> list[str]:
        """Valid permissions type for bucket defined in terraform module"""
        return [
            'bucketAdmin',
            'objectAdmin',
            'objectUser',
            'legacyBucketOwner',
            'legacyBucketReader',
            'legacyBucketWriter',
            'legacyObjectOwner',
            'legacyObjectReader',
            'objectCreator',
            'objectViewer',
            'cloudStorageOperator',
        ]
