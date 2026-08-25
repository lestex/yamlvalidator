import pytest

from src.config import get_config
from src.entities import get_entity
from src.validators.keyring import KeyringValidator


def test_keyring_fields():
    type_ = 'keyring'
    keyring = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(keyring)

    valid_fields = ['name']

    assert keyring.valid_fields == valid_fields
    assert keyring.class_name == 'keyring'


test_data = [
    # each tuple represents a test case
    (
        # valid keyring
        {
            'name': 'keyring001',
        },
        # filename
        'keyring001_keyring.yml',
        # validation result
        [],
    ),
    (
        # invalid keyring wrong filename
        {
            'name': 'keyring002',
        },
        # filename
        'keyring_keyring.yml',
        # validation result
        ['filename must be: keyring002_keyring.yml'],
    ),
    (
        # invalid keyring validate fields
        {
            'name': 'keyring003',
            'bad_field': 'test',
        },
        # filename
        'keyring003_keyring.yml',
        # validation result
        ["field:'bad_field' is not supported for keyring"],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_keyring(test_input, filename, expected, config_file):
    type_ = 'keyring'
    validator = KeyringValidator()

    keyring = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(keyring, cfg)

    assert sorted(validator.errors) == sorted(expected)


def test_keyring_duplicate_name(config_file):
    """The same name twice in one run is a duplicate.

    Uniqueness state belongs to the config, so both entities must be
    validated against the same one.
    """
    type_ = 'keyring'
    validator = KeyringValidator()
    cfg = get_config(config_file)
    cfg.update('filename', 'keyring003_keyring.yml')

    validator.validate(get_entity(type_)(name='keyring003'), cfg)
    assert validator.errors == []

    validator.validate(get_entity(type_)(name='keyring003'), cfg)
    assert validator.errors == [
        "A duplicate object with name 'keyring003' already exists"
    ]
