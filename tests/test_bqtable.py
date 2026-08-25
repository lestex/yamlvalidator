import pytest

from yamlvalidator.config import get_config
from yamlvalidator.entities import get_entity
from yamlvalidator.validators.bqtable import BQTableValidator


def test_bqtable_fields():
    type_ = 'bqtable'
    bqtable = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(bqtable)

    valid_bqdataset_fields = [
        'name',
        'role',
        'members',
        'dataset_id',
        'table_id',
    ]

    assert bqtable.valid_fields == valid_bqdataset_fields
    assert bqtable.class_name == 'bqtable'


test_data = [
    # each tuple represents a test case
    (
        # valid bq table role
        {
            'role': 'roles/bigquery.dataViewer1',
            'members': ['group:123@example.com'],
            'dataset_id': 'cares_base',
            'table_id': 'page_external',
        },
        # filename
        'page_external_bigquery_dataViewer1_bqtable.yml',
        # validation result
        [],
    ),
    (
        # invalid bq dataset role
        {
            'role': 'bigquery.dataViewer2',
            'members': [],
            'dataset_id': 'cares_base',
            'table_id': 'page_external',
        },
        # filename
        'page_external_bigquery_dataViewer2_bqtable.yml',
        # validation result
        ["'role' might be incorrect, must include 'roles/'"],
    ),
    (
        # invalid bq dataset role - checks the validate_members validation
        {
            'role': 'roles/bigquery.dataEditor1',
            'members': [
                'user:123@test.com',
                'group:123@test.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
            ],
            'dataset_id': 'cares_base',
            'table_id': 'page_external',
        },
        # filename
        'page_external_bigquery_dataEditor1_bqtable.yml',
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
            'role': 'roles/bigquery.user1',
            'bad_field': 'test',
            'dataset_id': 'cares_base',
            'table_id': 'page_external',
        },
        # filename
        'page_external_bigquery_user1_bqtable.yml',
        # validation result
        [
            "field:'bad_field' is not supported for bqtable",
        ],
    ),
    (
        # invalid bq dataset role - checks the validate_filename validation
        {
            'role': 'roles/bigquery.writer2',
            'members': [],
            'dataset_id': 'cares_base',
            'table_id': 'page_external',
        },
        # filename
        'test_role.yml',
        # validation result
        [
            'filename must be: page_external_bigquery_writer2_bqtable.yml',
        ],
    ),
    (
        # invalid bq dataset role duplicate members
        {
            'role': 'roles/test123',
            'members': [
                'group:123@example.com',
                'group:123@example.com',
            ],
            'dataset_id': 'cares_base',
            'table_id': 'page_external',
        },
        # filename
        'page_external_test123_bqtable.yml',
        # validation result
        [
            "'members' has a duplicate member 'group:123@example.com'",
        ],
    ),
    (
        # invalid bq dataset role dataset_id not set
        {
            'role': 'roles/test1234',
            'members': [],
            'table_id': 'page_external',
        },
        # filename
        'page_external_test1234_bqtable.yml',
        # validation result
        [
            "'dataset_id' must be set",
        ],
    ),
    (
        # invalid bq dataset role table_id not set
        {
            'role': 'roles/test12345',
            'members': [],
            'dataset_id': 'cares_base',
        },
        # filename
        'page_external_test12345_bqdataset.yml',
        # validation result
        [
            "'table_id' must be set",
        ],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_bqtable(test_input, filename, expected, config_file):
    type_ = 'bqtable'
    validator = BQTableValidator()

    role = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(role, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()


def test_role_wrong_member_entity(config_file):
    type_ = 'bqtable'
    validator = BQTableValidator()
    cfg = get_config(config_file)

    test_input, filename, expected = (
        # invalid role invalid member in permissions
        {
            'role': 'roles/testnotallowedhere2',
            'members': [
                'notallowed:123@example.com',
            ],
            'dataset_id': 'test_id',
            'table_id': 'page_external',
        },
        # filename
        'page_external_testnotallowedhere2_bqtable.yml',
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
