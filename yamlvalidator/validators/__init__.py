from yamlvalidator.validators.base import BaseValidator
from yamlvalidator.validators.bqdataset import BQDatasetValidator
from yamlvalidator.validators.bqtable import BQTableValidator
from yamlvalidator.validators.bucket import BucketValidator
from yamlvalidator.validators.key import KeyValidator
from yamlvalidator.validators.keyring import KeyringValidator
from yamlvalidator.validators.role import RoleValidator
from yamlvalidator.validators.secret import SecretValidator
from yamlvalidator.validators.service import ServiceValidator
from yamlvalidator.validators.service_account import ServiceAccountValidator


def get_validator(type_: str) -> BaseValidator:
    """Returns a supported Validator class by it's type"""
    validators = {
        'bucket': BucketValidator(),
        'secret': SecretValidator(),
        'role': RoleValidator(),
        'sa': ServiceAccountValidator(),
        'service': ServiceValidator(),
        'keyring': KeyringValidator(),
        'key': KeyValidator(),
        'bqdataset': BQDatasetValidator(),
        'bqtable': BQTableValidator(),
    }
    validator = validators[type_]
    return validator
