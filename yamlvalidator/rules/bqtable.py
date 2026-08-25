from yamlvalidator.config import Config
from yamlvalidator.entities.bqtable import BQTable
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules.permissions import _validate_members_unique
from yamlvalidator.rules.permissions import _validate_permissions_members_list


def validate_role(bqtable: BQTable, config: Config) -> list[str]:
    """Validates bqdataset role name properly set"""
    errors = []

    if bqtable.role:
        role_name = bqtable.role.split('/')
        if 'roles' not in role_name:
            errors.append("'role' might be incorrect, must include 'roles/'")
    return errors


def validate_dataset_id(bqtable: BQTable, config: Config) -> list[str]:
    """Validates dataset_id is set"""
    errors = []

    if not bqtable.dataset_id:
        errors.append("'dataset_id' must be set")
    return errors


def validate_table_id(bqtable: BQTable, config: Config) -> list[str]:
    """Validates table_id is set"""
    errors = []

    if not bqtable.table_id:
        errors.append("'table_id' must be set")
    return errors


def validate_fields(bqtable: BQTable, config: Config) -> list[str]:
    """Validates bqtable has only allowed fields"""
    fields = bqtable.to_dict()
    return _validate_fields(
        bqtable.class_name, bqtable.valid_fields, fields, config
    )


def validate_filename(bqtable: BQTable, config: Config) -> list[str]:
    """Validates bqdataset name present in the filename"""
    errors = []

    if bqtable.role and bqtable.table_id:
        role_name = bqtable.role.split('/')[-1].replace('.', '_')
        table_id = bqtable.table_id
        name = f'{table_id}_{role_name}'
        errors.extend(_validate_filename(name, bqtable.class_name, config))
    return errors


def validate_members_unique(bqtable: BQTable, config: Config) -> list[str]:
    """Validates role permissions members are unique"""
    return _validate_members_unique(bqtable.members, 'members', config)


def validate_permissions_members(
    bqtable: BQTable, config: Config
) -> list[str]:
    """Validates bucket permissions members"""
    return _validate_permissions_members_list(
        'members', bqtable.members, config
    )
