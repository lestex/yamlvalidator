import pytest

from src.config import get_config
from src.entities import get_entity
from src.validators.secret import SecretValidator


def test_secret_fields():
    type_ = 'secret'
    secret = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(secret)

    valid_secret_fields = [
        'name',
        'permissions',
        'team',
        'category',
        'labels',
        'replicas',
    ]

    assert secret.valid_fields == valid_secret_fields
    assert secret.class_name == 'secret'

    secret_valid_permissions = [
        'secretAdmin',
        'secretAccessor',
        'secretVersionAdder',
        'secretVersionManager',
        'secretViewer',
    ]

    assert secret.permission_types == secret_valid_permissions


test_data = [
    # each tuple represents a test case
    (
        # valid secret with no team set
        {
            'name': 'test001',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
        },
        # filename
        'test001_secret.yml',
        # validation result
        [
            'Team must be set',
        ],
    ),
    (
        # invalid secret wrong filename
        {
            'name': 'test002',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
        },
        # filename
        'test001_sa.yml',
        # validation result
        ['Team must be set', 'filename must be: test002_secret.yml'],
    ),
    (
        # invalid secret validate fields
        {
            'name': 'test003',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
            'bad_field': 'test',
        },
        # filename
        'test003_secret.yml',
        # validation result
        [
            'Team must be set',
            "field:'bad_field' is not supported for secret",
        ],
    ),
    (
        # invalid secret - checks the validate_members validation
        {
            'name': 'test004',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
            'permissions': {'notKnown': []},
        },
        # filename
        'test004_secret.yml',
        # validation result
        [
            'Team must be set',
            "'notKnown' is not valid, must be ['secretAdmin', 'secretAccessor', "
            "'secretVersionAdder', 'secretVersionManager', 'secretViewer']",
        ],
    ),
    (
        # invalid secret - checks the validate_members validation
        {
            'name': 'test005',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'secretAccessor': [
                    'user:123@test.com',
                    'group:123@test.com',
                    'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
                ]
            },
        },
        # filename
        'test005_secret.yml',
        # validation result
        [
            'Team must be set',
            'invalid Service Account',
            "only groups from ['example.com'] are allowed",
            '123@test.com must not be used here, only specific users or users from '
            "['partner.example.com'] allowed, use 'group' instead",
        ],
    ),
    (
        # invalid secret diplicate members
        {
            'name': 'test006',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'secretAccessor': [
                    'group:123@example.com',
                    'group:123@example.com',
                ]
            },
        },
        # filename
        'test006_secret.yml',
        # validation result
        [
            'Team must be set',
            "'permissions':'secretAccessor' has a duplicate member "
            "'group:123@example.com'",
        ],
    ),
    (
        # invalid secret category not set
        {
            'name': 'test009',
            'team': '',
        },
        # filename
        'test009_secret.yml',
        # validation result
        [
            'Category must be set',
            'Team must be set',
            "at least 'app1' label must be set",
        ],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_secret(test_input, filename, expected, config_file):
    type_ = 'secret'
    validator = SecretValidator()

    secret = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(secret, cfg)

    assert sorted(validator.errors) == sorted(expected)


def test_secret_wrong_member_entity(config_file):
    type_ = 'secret'
    validator = SecretValidator()
    cfg = get_config(config_file)

    test_input, filename, expected = (
        # invalid secret invalid members
        {
            'name': 'test008',
            'team': '',
            'category': 'test_category',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'secretAccessor': [
                    'notallowed:123@example.com',
                ]
            },
        },
        # filename
        'test008_secret.yml',
        # validation result
        [
            'Team must be set',
            "'notallowed' is not allowed in 'secretAccessor', "
            f'must be {sorted(cfg.allowed_types)}',
        ],
    )

    secret = get_entity(type_)(**test_input)
    cfg.update('filename', filename)

    validator.validate(secret, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()


def test_secret_duplicate_name(config_file):
    """The same name twice in one run is a duplicate.

    Uniqueness state belongs to the config, so both entities must be
    validated against the same one.
    """
    type_ = 'secret'
    validator = SecretValidator()
    cfg = get_config(config_file)
    cfg.update('filename', 'test005_secret.yml')
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    test_input = {
        'name': 'test005',
        'team': 'team',
        'category': 'test_category',
        'labels': {'app1': 'set'},
    }

    validator.validate(get_entity(type_)(**test_input), cfg)
    validator.clear()

    validator.validate(get_entity(type_)(**test_input), cfg)
    assert (
        "A duplicate object with name 'test005' already exists"
        in validator.errors
    )
