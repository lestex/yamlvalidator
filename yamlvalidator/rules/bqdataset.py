from yamlvalidator.config import Config
from yamlvalidator.entities.bqdataset import BQDataset
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules.permissions import _validate_members_unique
from yamlvalidator.rules.permissions import _validate_permissions_members_list


def validate_role(bqdataset: BQDataset, config: Config) -> list[str]:
    """Validates bqdataset role name properly set"""
    errors = []

    if bqdataset.role:
        role_name = bqdataset.role.split('/')
        if 'roles' not in role_name:
            errors.append("'role' might be incorrect, must include 'roles/'")
    return errors


def validate_fields(bqdataset: BQDataset, config: Config) -> list[str]:
    """Validates bqdataset has only allowed fields"""
    fields = bqdataset.to_dict()
    return _validate_fields(
        bqdataset.class_name, bqdataset.valid_fields, fields, config
    )


def validate_filename(bqdataset: BQDataset, config: Config) -> list[str]:
    """Validates bqdataset name present in the filename"""
    errors = []

    if bqdataset.role and bqdataset.dataset_id:
        role_name = bqdataset.role.split('/')[-1].replace('.', '_')
        dataset_id = bqdataset.dataset_id
        name = f'{dataset_id}_{role_name}'
        errors.extend(_validate_filename(name, bqdataset.class_name, config))
    return errors


def validate_members_unique(bqdataset: BQDataset, config: Config) -> list[str]:
    """Validates role permissions members are unique"""
    return _validate_members_unique(bqdataset.members, 'members', config)


def validate_permissions_members(
    bqdataset: BQDataset, config: Config
) -> list[str]:
    """Validates bucket permissions members"""
    return _validate_permissions_members_list(
        'members', bqdataset.members, config
    )
