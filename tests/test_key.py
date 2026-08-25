import pytest

from src.config import get_config
from src.entities import get_entity
from src.rules.key import MIN_ROTATION_PERIOD_SECONDS
from src.rules.key import VALID_KEYPURPOSE
from src.rules.key import VALID_PROTECTION_LEVELS
from src.rules.key import validate_key_rotation_period
from src.validators.key import KeyValidator


def test_key_fields():
    type_ = 'key'
    key = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(key)

    valid_fields = [
        'name',
        'keyring_name',
        'key_purpose',
        'key_rotation_period',
        'is_version_template',
        'algorithm',
        'protection_level',
        'cryptoKeyDecrypter',
        'cryptoKeyEncrypter',
        'cryptoKeyEncrypterDecrypter',
        'importer',
        'keyAdmin',
        'publicKeyViewer',
        'signer',
        'signerVerifier',
    ]

    assert key.valid_fields == valid_fields
    assert key.class_name == 'key'


test_data = [
    # each tuple represents a test case
    (
        # valid key
        {
            'name': 'key001',
            'keyring_name': 'keyring_name',
        },
        # filename
        'key001_key.yml',
        # validation result
        [],
    ),
    (
        # invalid key no keyring set
        {
            'name': 'key002',
        },
        # filename
        'key002_key.yml',
        # validation result
        ["'keyring_name' must be set"],
    ),
    (
        # invalid key wrong filename
        {
            'name': 'key003',
            'keyring_name': 'keyring_name',
        },
        # filename
        'key_key.yml',
        # validation result
        ['filename must be: key003_key.yml'],
    ),
    (
        # invalid key validate fields
        {
            'name': 'key004',
            'keyring_name': 'keyring_name',
            'bad_field': 'test',
        },
        # filename
        'key004_key.yml',
        # validation result
        ["field:'bad_field' is not supported for key"],
    ),
    (
        # invalid key
        {
            'name': 'key005',
            'keyring_name': 'keyring_name',
            'is_version_template': True,
        },
        # filename
        'key005_key.yml',
        # validation result
        [
            "'algorithm' and 'protection_level' must be set "
            "when 'is_version_template' is set",
        ],
    ),
    (
        # invalid key
        {
            'name': 'key006',
            'keyring_name': 'keyring_name',
            'is_version_template': True,
        },
        # filename
        'key006_key.yml',
        # validation result
        [
            "'algorithm' and 'protection_level' must be set "
            "when 'is_version_template' is set",
        ],
    ),
    (
        # invalid key
        {
            'name': 'key007',
            'keyring_name': 'keyring_name',
            'is_version_template': True,
        },
        # filename
        'key007_key.yml',
        # validation result
        [
            "'algorithm' and 'protection_level' must be set "
            "when 'is_version_template' is set",
        ],
    ),
    (
        # invalid key
        {
            'name': 'key008',
            'keyring_name': 'keyring_name',
            'key_rotation_period': '1234s',
        },
        # filename
        'key008_key.yml',
        # validation result
        ["'key_rotation_period' must be at least 86400 seconds"],
    ),
    (
        # invalid key
        {
            'name': 'key009',
            'keyring_name': 'keyring_name',
            'key_rotation_period': '1234',
        },
        # filename
        'key009_key.yml',
        # validation result
        [
            "'key_rotation_period' must be a decimal number with up to "
            "9 digits, followed by the letter 's'"
        ],
    ),
    (
        # invalid key
        {
            'name': 'key010',
            'keyring_name': 'keyring_name',
            'importer': [
                'serviceAccount:pl-terraform@my-org-infra-prod.iam.gserviceaccount.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam.gserviceaccount.com',
            ],
        },
        # filename
        'key010_key.yml',
        # validation result
        [
            "'importer' has a duplicate member "
            "'serviceAccount:pl-terraform@my-org-infra-prod.iam.gserviceaccount.com'"
        ],
    ),
    (
        # invalid key
        {
            'name': 'key011',
            'keyring_name': 'keyring_name',
            'keyAdmin': [
                'serviceAccount:pl-terraform@my-org-infra-prod.iam.gserviceaccount.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam.gserviceaccount.com',
            ],
        },
        # filename
        'key011_key.yml',
        # validation result
        [
            "'keyAdmin' has a duplicate member "
            "'serviceAccount:pl-terraform@my-org-infra-prod.iam.gserviceaccount.com'"
        ],
    ),
    (
        # invalid key with wrong permisssions member
        {
            'name': 'key012',
            'keyring_name': 'keyring_name',
            'cryptoKeyDecrypter': [
                '123@example.com',
            ],
        },
        # filename
        'key012_key.yml',
        # validation result
        [
            'Invalid entity: 123@example.com',
        ],
    ),
    (
        # invalid key with wrong permisssions member
        {
            'name': 'key013',
            'keyring_name': 'keyring_name',
            'publicKeyViewer': [
                '123@example.com',
            ],
        },
        # filename
        'key013_key.yml',
        # validation result
        [
            'Invalid entity: 123@example.com',
        ],
    ),
    (
        # invalid key with wrong key_purpose
        {
            'name': 'key014',
            'keyring_name': 'keyring_name',
            'key_purpose': 'INVALID',
        },
        # filename
        'key014_key.yml',
        # validation result
        [
            f'invalid key purpose set, must be one of: {VALID_KEYPURPOSE}',
        ],
    ),
    (
        # invalid key with wrong algorithm
        {
            'name': 'key015',
            'keyring_name': 'keyring_name',
            'algorithm': 'INVALID',
        },
        # filename
        'key015_key.yml',
        # validation result
        [
            "'is_version_template' must be also set when 'algorithm' is set",
            "invalid 'algorithm' set, see "
            "'https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm'",
        ],
    ),
    (
        # invalid key with wrong protection_level
        {
            'name': 'key016',
            'keyring_name': 'keyring_name',
            'protection_level': 'INVALID',
        },
        # filename
        'key016_key.yml',
        # validation result
        [
            "'is_version_template' must be also set "
            "when 'protection_level' is set",
            "invalid 'protection_level' set, must be "
            f'one of: {VALID_PROTECTION_LEVELS}',
        ],
    ),
    (
        # valid key
        {
            'name': 'key017',
            'keyring_name': 'keyring_name',
            'is_version_template': True,
            'protection_level': 'SOFTWARE',
            'algorithm': 'GOOGLE_SYMMETRIC_ENCRYPTION',
        },
        # filename
        'key017_key.yml',
        # validation result
        [],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_key(test_input, filename, expected, config_file):
    type_ = 'key'
    validator = KeyValidator()

    keyring = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(keyring, cfg)

    assert sorted(validator.errors) == sorted(expected)


@pytest.mark.parametrize(
    'period,expected',
    [
        # one second under a day is rejected
        (f'{MIN_ROTATION_PERIOD_SECONDS - 1}s', False),
        # exactly a day is accepted
        (f'{MIN_ROTATION_PERIOD_SECONDS}s', True),
        # the transposed 84600 used to let this through
        ('85000s', False),
    ],
)
def test_key_rotation_period_boundary(period, expected, config_file):
    """The threshold is 86400, not the transposed 84600."""
    key = get_entity('key')(name='key100', key_rotation_period=period)
    cfg = get_config(config_file)

    errors = validate_key_rotation_period(key, cfg)

    assert (errors == []) is expected


def test_key_duplicate_name(config_file):
    """The same name twice in one run is a duplicate.

    Uniqueness state belongs to the config, so both entities must be
    validated against the same one.
    """
    type_ = 'key'
    validator = KeyValidator()
    cfg = get_config(config_file)
    cfg.update('filename', 'key004_key.yml')
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    test_input = {'name': 'key004', 'keyring_name': 'keyring_name'}

    validator.validate(get_entity(type_)(**test_input), cfg)
    validator.clear()

    validator.validate(get_entity(type_)(**test_input), cfg)
    assert (
        "A duplicate object with name 'key004' already exists"
        in validator.errors
    )
