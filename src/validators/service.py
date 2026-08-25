from typing import Callable

from src.config import Config
from src.entities.service import Service
from src.rules.service import validate_disable_on_destroy
from src.rules.service import validate_fields
from src.rules.service import validate_filename
from src.rules.service import validate_service
from src.rules.service import validate_service_key
from src.validators.base import BaseValidator

# dictionary holds all validation functions to be run agains service entity
checks: dict[str, Callable[[Service, Config], list[str]]] = {
    'validate_service': validate_service,
    'validate_disable_on_destroy': validate_disable_on_destroy,
    'validate_service_key': validate_service_key,
    'validate_fields': validate_fields,
    'validate_filename': validate_filename,
}


class ServiceValidator(BaseValidator):
    """Service validator class"""

    checks: dict = checks.copy()
