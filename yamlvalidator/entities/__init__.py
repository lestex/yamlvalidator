import importlib

from yamlvalidator.entities.bqdataset import BQDataset
from yamlvalidator.entities.bqtable import BQTable
from yamlvalidator.entities.bucket import Bucket
from yamlvalidator.entities.key import Key
from yamlvalidator.entities.keyring import Keyring
from yamlvalidator.entities.role import Role
from yamlvalidator.entities.secret import Secret
from yamlvalidator.entities.service import Service
from yamlvalidator.entities.service_account import ServiceAccount


def get_supported_entities() -> list[str]:
    modules = importlib.import_module('yamlvalidator.entities')
    return sorted(
        [
            cls_().class_name
            for _, cls_ in modules.__dict__.items()
            if isinstance(cls_, type)
        ]
    )


def get_entity(type_: str) -> type:
    """Returns a supported entity class by it's type"""
    entities = {
        'bucket': Bucket,
        'secret': Secret,
        'role': Role,
        'sa': ServiceAccount,
        'service': Service,
        'keyring': Keyring,
        'key': Key,
        'bqdataset': BQDataset,
        'bqtable': BQTable,
    }
    entity = entities[type_]
    return entity
