import pytest

from src.config import get_config
from src.entities import get_entity
from src.validators.role import RoleValidator


def test_role_fields():
    type_ = 'role'
    role = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(role)

    valid_role_fields = [
        'name',
        'role',
        'members',
    ]

    assert role.valid_fields == valid_role_fields
    assert role.class_name == 'role'


test_data = [
    # each tuple represents a test case
    (
        # valid role
        {
            'role': 'roles/browser',
            'members': ['group:123@example.com'],
        },
        # filename
        'browser_role.yml',
        # validation result
        [],
    ),
    (
        # invalid role - checks the validate_role validation
        {
            'role': 'browser',
            'members': [],
        },
        # filename
        'browser_role.yml',
        # validation result
        ["'role' might be incorrect, must include 'roles/'"],
    ),
    (
        # invalid role - checks the validate_members validation
        {
            'role': 'roles/viewer',
            'members': [
                'user:123@test.com',
                'group:123@test.com',
                'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
            ],
        },
        # filename
        'viewer_role.yml',
        # validation result
        [
            'invalid Service Account',
            "only groups from ['example.com'] are allowed",
            '123@test.com must not be used here, only specific users or users from '
            "['partner.example.com'] allowed, use 'group' instead",
        ],
    ),
    (
        # invalid role - checks the validate_fields validation
        {
            'role': 'roles/compute.admin',
            'bad_field': 'test',
        },
        # filename
        'compute_admin_role.yml',
        # validation result
        [
            "field:'bad_field' is not supported for role",
        ],
    ),
    (
        # invalid role - checks the validate_filename validation
        {
            'role': 'projects/my-org-arc-poc/roles/project_cloudsqlUserEditor',
            'members': [],
        },
        # filename
        'test_role.yml',
        # validation result
        [
            'filename must be: project_cloudsqlUserEditor_role.yml',
        ],
    ),
    (
        # invalid role duplicate validation
        {
            'role': 'roles/browser',
        },
        # filename
        'browser_role.yml',
        # validation result
        [
            "A duplicate object with name 'roles/browser' already exists",
        ],
    ),
    (
        # invalid role duplicate members
        {
            'role': 'roles/test',
            'members': [
                'group:123@example.com',
                'group:123@example.com',
            ],
        },
        # filename
        'test_role.yml',
        # validation result
        [
            "'members' has a duplicate member 'group:123@example.com'",
        ],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_role(test_input, filename, expected, config_file):
    type_ = 'role'
    validator = RoleValidator()

    role = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(role, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()


def test_role_wrong_member_entity(config_file):
    type_ = 'role'
    validator = RoleValidator()
    cfg = get_config(config_file)

    test_input, filename, expected = (
        # invalid role invalid member in permissions
        {
            'role': 'roles/testnotallowed',
            'members': [
                'notallowed:123@example.com',
            ],
        },
        # filename
        'testnotallowed_role.yml',
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
