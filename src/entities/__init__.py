import importlib

from src.entities.bucket import Bucket
from src.entities.keyring import Keyring
from src.entities.role import Role
from src.entities.secret import Secret
from src.entities.service import Service
from src.entities.service_account import ServiceAccount


def get_supported_entities() -> list[str]:
    modules = importlib.import_module('src.entities')
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
    }
    entity = entities[type_]
    return entity
