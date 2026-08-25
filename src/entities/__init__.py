import importlib


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

    }
    entity = entities[type_]
    return entity
