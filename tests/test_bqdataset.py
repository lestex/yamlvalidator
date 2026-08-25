import pytest

from yamlvalidator.config import get_config
from yamlvalidator.entities import get_entity
from yamlvalidator.validators.bqdataset import BQDatasetValidator


def test_bqdataset_fields():
    type_ = 'bqdataset'
    bqdataset = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(bqdataset)

    valid_bqdataset_fields = [
        'name',
        'role',
        'members',
        'dataset_id',
    ]

    assert bqdataset.valid_fields == valid_bqdataset_fields
    assert bqdataset.class_name == 'bqdataset'


test_data = [
    # each tuple represents a test case
    (
        # valid bq dataset role
        {
            'role': 'roles/bigquery.dataViewer',
            'members': ['group:123@example.com'],
            'dataset_id': 'common_base',
        },
        # filename
        'common_base_bigquery_dataViewer_bqdataset.yml',
        # validation result
        [],
    ),
    (
        # invalid bq dataset role
        {
            'role': 'bigquery.dataViewer',
            'members': [],
            'dataset_id': 'common_base',
        },
        # filename
        'common_base_bigquery_dataViewer_bqdataset.yml',
        # validation result
        ["'role' might be incorrect, must include 'roles/'"],
    ),
    (
        # invalid bq dataset role - checks the validate_members validation
        {
            'role': 'roles/bigquery.dataEditor',
            'members': [
                'user:123@test.com',
                'group:123@test.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
            ],
            'dataset_id': 'common_base',
        },
        # filename
        'common_base_bigquery_dataEditor_bqdataset.yml',
        # validation result
        [
            'invalid Service Account',
            "only groups from ['example.com'] are allowed",
            '123@test.com must not be used here, only specific users or users from '
            "['partner.example.com'] allowed, use 'group' instead",
        ],
    ),
    (
        # invalid bq dataset role - checks the validate_fields validation
        {
            'role': 'roles/bigquery.user',
            'bad_field': 'test',
            'dataset_id': 'common_base',
        },
        # filename
        'common_base_bigquery_user_bqdataset.yml',
        # validation result
        [
            "field:'bad_field' is not supported for bqdataset",
        ],
    ),
    (
        # invalid bq dataset role - checks the validate_filename validation
        {
            'role': 'roles/bigquery.writer',
            'members': [],
            'dataset_id': 'common_base',
        },
        # filename
        'test_role.yml',
        # validation result
        [
            'filename must be: common_base_bigquery_writer_bqdataset.yml',
        ],
    ),
    (
        # invalid bq dataset role duplicate members
        {
            'role': 'roles/test1',
            'members': [
                'group:123@example.com',
                'group:123@example.com',
            ],
            'dataset_id': 'test_id',
        },
        # filename
        'test_id_test1_bqdataset.yml',
        # validation result
        [
            "'members' has a duplicate member 'group:123@example.com'",
        ],
    ),
    (
        # invalid bq dataset role dataset_id not set
        {
            'role': 'roles/test12',
            'members': [],
        },
        # filename
        'test_id_test12_bqdataset.yml',
        # validation result
        [
            "'dataset_id' must be set",
        ],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_bqdataset(test_input, filename, expected, config_file):
    type_ = 'bqdataset'
    validator = BQDatasetValidator()

    role = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(role, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()


def test_role_wrong_member_entity(config_file):
    type_ = 'bqdataset'
    validator = BQDatasetValidator()
    cfg = get_config(config_file)

    test_input, filename, expected = (
        # invalid role invalid member in permissions
        {
            'role': 'roles/testnotallowedhere',
            'members': [
                'notallowed:123@example.com',
            ],
            'dataset_id': 'test_id',
        },
        # filename
        'test_id_testnotallowedhere_bqdataset.yml',
        # validation result
        [
            "'notallowed' is not allowed in 'members', "
            f'must be {sorted(cfg.allowed_types)}',
        ],
    )

    role = get_entity(type_)(**test_input)
    cfg.update('filename', filename)

    validator.validate(role, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()
