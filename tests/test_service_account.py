import pytest

from src.config import get_config
from src.entities import get_entity
from src.validators.service_account import ServiceAccountValidator


def test_service_account_fields():
    type_ = 'sa'
    sa = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(sa)

    valid_sa_fields = [
        'name',
        'account_id',
        'disabled',
        'display_name',
        'description',
        'serviceAccountUser',
        'workloadIdentityUser',
    ]

    assert sa.valid_fields == valid_sa_fields
    assert sa.class_name == 'sa'


test_data = [
    (
        # valid service account
        {
            'account_id': 'pl-testsa001',
        },
        # filename
        'pl-testsa001_sa.yml',
        # validation result
        [],
    ),
    (
        # invalid service account validate account_id
        {
            'account_id': 'testsa002',
        },
        # filename
        'testsa002_sa.yml',
        # validation result
        [
            "'account_id' is incorrect, must include 'pl-'",
        ],
    ),
    (
        # invalid service account validate serviceAccountUser
        {
            'account_id': 'pl-testsa003',
            'serviceAccountUser': [
                'user:123@test.com',
                'group:123@test.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
            ],
        },
        # filename
        'pl-testsa003_sa.yml',
        # validation result
        [
            'invalid Service Account',
            "only groups from ['example.com'] are allowed",
            '123@test.com must not be used here, only specific users or users from '
            "['partner.example.com'] allowed, use 'group' instead",
        ],
    ),
    (
        # invalid service account validate workloadIdentityUser
        {
            'account_id': 'pl-testsa004',
            'workloadIdentityUser': [
                'user:123@test.com',
                'group:123@test.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
            ],
        },
        # filename
        'pl-testsa004_sa.yml',
        # validation result
        [
            'invalid Service Account',
            "only groups from ['example.com'] are allowed",
            '123@test.com must not be used here, only specific users or users from '
            "['partner.example.com'] allowed, use 'group' instead",
        ],
    ),
    (
        # invalid service account validate fields
        {
            'account_id': 'pl-testsa005',
            'bad_field': 'test',
        },
        # filename
        'pl-testsa005_sa.yml',
        # validation result
        [
            "field:'bad_field' is not supported for sa",
        ],
    ),
    (
        # invalid service account validate filename
        {
            'account_id': 'pl-testsa006',
        },
        # filename
        'test_role.yml',
        # validation result
        [
            'filename must be: pl-testsa006_sa.yml',
        ],
    ),
    (
        # invalid service account validate description if set to ''
        {
            'account_id': 'pl-testsa007',
            'description': '',
            'display_name': '',
        },
        # filename
        'pl-testsa007_sa.yml',
        # validation result
        [
            "'description' must be set",
            "'display_name' must be set",
        ],
    ),
    (
        # valid service account
        {
            'account_id': 'pl-testsa008',
            'workloadIdentityUser': [
                'serviceAccount:my-org-kube-dev.svc.id.goog[rc/hello-container-ksa]',
            ],
        },
        # filename
        'pl-testsa008_sa.yml',
        # validation result
        [],
    ),
    (
        # invalid service account 'disabled' validation
        {
            'account_id': 'pl-test-disable',
            'disabled': 'Aye',
        },
        # filename
        'pl-test-disable_sa.yml',
        # validation result
        [
            "value of 'disabled' is incorrect, must be boolean",
        ],
    ),
    (
        # invalid service account 'disabled' validation
        {
            'account_id': 'pl-test-disable-successful',
            'disabled': True,
        },
        # filename
        'pl-test-disable-successful_sa.yml',
        # validation result
        [],
    ),
    (
        # invalid service members workloadIdentityUser
        {
            'account_id': 'pl-test',
            'workloadIdentityUser': [
                'group:123@example.com',
                'group:123@example.com',
            ],
        },
        # filename
        'pl-test_sa.yml',
        # validation result
        [
            "'workloadIdentityUser' has a duplicate member 'group:123@example.com'"
        ],
    ),
    (
        # invalid service members serviceAccountUser
        {
            'account_id': 'pl-test1',
            'serviceAccountUser': [
                'group:123@example.com',
                'group:123@example.com',
            ],
        },
        # filename
        'pl-test1_sa.yml',
        # validation result
        [
            "'serviceAccountUser' has a duplicate member 'group:123@example.com'"
        ],
    ),
    (
        # test ml service accounts
        {
            'account_id': 'pl-ml-google',
            'serviceAccountUser': [
                'serviceAccount:123456789012@cloud-ml.google.com.iam.gserviceaccount.com',
            ],
        },
        # filename
        'pl-ml-google_sa.yml',
        # validation result
        [],
    ),
    (
        # service account disabled
        {
            'account_id': 'pl-test-disabled',
            'disabled': 'wrong',
        },
        # filename
        'pl-test-disabled_sa.yml',
        # validation result
        ["value of 'disabled' is incorrect, must be boolean"],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_service_account(test_input, filename, expected, config_file):
    type_ = 'sa'
    validator = ServiceAccountValidator()

    sa = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(sa, cfg)

    assert sorted(validator.errors) == sorted(expected)


def test_service_account_wrong_member_entity(config_file):
    type_ = 'sa'
    validator = ServiceAccountValidator()
    cfg = get_config(config_file)

    test_input, filename, expected = (
        # invalid service members serviceAccountUser
        {
            'account_id': 'pl-test12',
            'serviceAccountUser': [
                'notallowed:123@example.com',
            ],
        },
        # filename
        'pl-test12_sa.yml',
        # validation result
        [
            f"'notallowed' is not allowed in 'serviceAccountUser', "
            f'must be {sorted(cfg.allowed_types)}'
        ],
    )

    sa = get_entity(type_)(**test_input)
    cfg.update('filename', filename)

    validator.validate(sa, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()


def test_service_account_duplicate_name(config_file):
    """The same name twice in one run is a duplicate.

    Uniqueness state belongs to the config, so both entities must be
    validated against the same one.
    """
    type_ = 'sa'
    validator = ServiceAccountValidator()
    cfg = get_config(config_file)
    cfg.update('filename', 'pl-testsa007_sa.yml')
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    test_input = {'account_id': 'pl-testsa007'}

    validator.validate(get_entity(type_)(**test_input), cfg)
    validator.clear()

    validator.validate(get_entity(type_)(**test_input), cfg)
    assert (
        "A duplicate object with name 'pl-testsa007' already exists"
        in validator.errors
    )
