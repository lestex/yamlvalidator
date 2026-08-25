import pytest

from src.validators import get_validator
from src.validators.bucket import BucketValidator
from src.validators.role import RoleValidator
from src.validators.secret import SecretValidator
from src.validators.service_account import ServiceAccountValidator

test_data = [
    # type, result
    ('bucket', BucketValidator),
    ('secret', SecretValidator),
    ('role', RoleValidator),
    ('sa', ServiceAccountValidator),
]


@pytest.mark.parametrize('test_input,expected', test_data)
def test_get_validator_returns_not_none(test_input, expected):
    type_ = test_input
    validator = get_validator(type_)

    assert validator is not None
    assert issubclass(type(validator), expected)


@pytest.mark.parametrize('test_input,expected', test_data)
def test_validator_properties(test_input, expected):
    type_ = test_input
    validator = get_validator(type_)

    assert 'checks' and 'errors' in dir(validator)

    validator.errors.extend(['test'])
    assert 'test' in validator.errors

    validator.clear()
    assert validator.errors == []


def test_validator_errors_are_not_shared():
    """Errors must not leak between validator instances or subclasses."""
    bucket = get_validator('bucket')
    secret = get_validator('secret')
    another_bucket = get_validator('bucket')

    bucket.errors.append('test')

    assert secret.errors == []
    assert another_bucket.errors == []
