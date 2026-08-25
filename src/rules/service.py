from src.config import Config
from src.entities.service import Service
from src.rules import _validate_fields


def validate_service(entity: Service, config: Config) -> list[str]:
    """Validate object `service` (api name) is valid"""
    errors: list[str] = []
    if not entity.service:
        errors.append("'service' field must be set")
    return errors


def validate_disable_on_destroy(entity: Service, config: Config) -> list[str]:
    """Validate object `validate_disable_on_destroy` is valid"""
    errors: list[str] = []
    if entity.disable_on_destroy and not isinstance(
        entity.disable_on_destroy, bool
    ):
        errors.append(
            "'disable_on_destroy' must be bool ['false'"
            ' is default and can be omitted]'
        )
    return errors


def validate_service_key(entity: Service, config: Config) -> list[str]:
    """Validate object's key is valid"""
    errors: list[str] = []
    if entity.service:
        key = entity.service.replace('.', '_')
        obj_key = config.obj_name
        if key != obj_key:
            errors.append(f'{obj_key!r} is incorrect, must be: {key}')
    return errors


def validate_filename(entity: Service, config: Config) -> list[str]:
    """Validate object's key is valid"""
    errors: list[str] = []
    filename = config.filename
    valid_filename = 'apis_service.yml'
    if filename != valid_filename:
        errors.append(
            f'filename {filename!r} is incorrect, must be: {valid_filename}'
        )
    return errors


def validate_fields(entity: Service, config: Config) -> list[str]:
    """Validates object fields are same as defined in dataclass"""
    fields = entity.to_dict()
    return _validate_fields(
        entity.class_name, entity.valid_fields, fields, config
    )
