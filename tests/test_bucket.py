import pytest

from yamlvalidator.config import get_config
from yamlvalidator.entities import get_entity
from yamlvalidator.validators.bucket import BucketValidator


def test_bucket_fields():
    type_ = 'bucket'
    bucket = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(bucket)

    valid_bucket_fields = [
        'name',
        'permissions',
        'team',
        'bucket_name',
        'cors',
        'default_kms_key_name',
        'folders',
        'force_destroy',
        'hmac_service_accounts',
        'labels',
        'lifecycle_rules',
        'location',
        'log_bucket',
        'log_object_prefix',
        'notification_event_types',
        'notification_payload',
        'notification_object_name_prefix',
        'requester_pays',
        'retention_policy',
        'storage_class',
        'storage_class_backup',
        'topic',
        'topic_serviceaccount',
        'uniform_bucket_level_access',
        'versioning',
        'website',
        'description',
        'enable_backup_bucket',
        'schedule',
        'transfer_spec',
        'autoclass_enable',
        'terminal_storage_class',
    ]

    assert bucket.valid_fields == valid_bucket_fields
    assert bucket.class_name == 'bucket'

    bucket_valid_permissions = [
        'bucketAdmin',
        'objectAdmin',
        'objectUser',
        'legacyBucketOwner',
        'legacyBucketReader',
        'legacyBucketWriter',
        'legacyObjectOwner',
        'legacyObjectReader',
        'objectCreator',
        'objectViewer',
        'cloudStorageOperator',
    ]
    assert bucket.permission_types == bucket_valid_permissions


test_data = [
    # each tuple represents a test case
    (
        # valid bucket
        {
            'name': 'bucket001',
            'team': '',
            'labels': {'app1': 'not-set'},
        },
        # filename
        'bucket001_bucket.yml',
        # validation result
        [
            "'team' must be set",
        ],
    ),
    (
        # invalid bucket wrong filename
        {
            'name': 'bucket002',
            'team': '',
            'labels': {'app1': 'not-set'},
        },
        # filename
        'bucket_bucket.yml',
        # validation result
        ["'team' must be set", 'filename must be: bucket002_bucket.yml'],
    ),
    (
        # invalid bucket validate fields
        {
            'name': 'bucket003',
            'team': '',
            'labels': {'app1': 'not-set'},
            'bad_field': 'test',
        },
        # filename
        'bucket003_bucket.yml',
        # validation result
        [
            "'team' must be set",
            "field:'bad_field' is not supported for bucket",
        ],
    ),
    (
        # invalid bucket bad permissions
        {
            'name': 'bucket004',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {'notKnown': []},
        },
        # filename
        'bucket004_bucket.yml',
        # validation result
        [
            "'team' must be set",
            "'notKnown' is not valid, must be ['bucketAdmin', 'objectAdmin', 'objectUser', "
            "'legacyBucketOwner', 'legacyBucketReader', 'legacyBucketWriter', "
            "'legacyObjectOwner', 'legacyObjectReader', 'objectCreator', "
            "'objectViewer', 'cloudStorageOperator']",
        ],
    ),
    (
        # invalid bucket permission validation
        {
            'name': 'bucket005',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'objectAdmin': [
                    'user:123@test.com',
                    'group:123@test.com',
                    'serviceAccount:pl-terraform@my-org-infra-prod.iam2.gserviceaccount.com',
                ]
            },
        },
        # filename
        'bucket005_bucket.yml',
        # validation result
        [
            "'team' must be set",
            'invalid Service Account',
            "only groups from ['example.com'] are allowed",
            '123@test.com must not be used here, only specific users or users from '
            "['partner.example.com'] allowed, use 'group' instead",
        ],
    ),
    (
        # invalid bucket permission validation
        {
            'name': '',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'objectAdmin': [
                    'allAuthenticatedUsers',
                    'allUsers',
                ]
            },
        },
        # filename
        '_bucket.yml',
        # validation result
        [
            "'name' must be set",
            "'team' must be set",
        ],
    ),
    (
        # invalid bucket duplicate members in permissions
        {
            'name': 'bucket006',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'bucketAdmin': [
                    'group:123@example.com',
                    'group:123@example.com',
                ],
            },
        },
        # filename
        'bucket006_bucket.yml',
        # validation result
        [
            "'team' must be set",
            "'permissions':'bucketAdmin' has a duplicate member "
            "'group:123@example.com'",
        ],
    ),
    (
        # valid bucket with allUsers permission
        {
            'name': 'bucket008',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'bucketAdmin': [
                    'allUsers',
                    'group:123@example.com',
                    'allAuthenticatedUsers',
                ],
            },
        },
        # filename
        'bucket008_bucket.yml',
        # validation result
        [
            "'team' must be set",
        ],
    ),
    (
        # invalid bucket with wrong permisssions member
        {
            'name': 'bucket009',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'bucketAdmin': [
                    '123@example.com',
                ],
            },
        },
        # filename
        'bucket009_bucket.yml',
        # validation result
        [
            'Invalid entity: 123@example.com',
            "'team' must be set",
        ],
    ),
    (
        {
            # bucket with service account non my-org
            'name': 'bucket010',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'objectAdmin': [
                    'serviceAccount:example@my-org-box-dev.iam.gserviceaccount.com',
                    'serviceAccount:wrong@cloudservices.gserviceaccount.com',
                ]
            },
        },
        # filename
        'bucket010_bucket.yml',
        # validation result
        [
            "'team' must be set",
        ],
    ),
]


@pytest.mark.parametrize('test_input,filename,expected', test_data)
def test_bucket(test_input, filename, expected, config_file):
    type_ = 'bucket'
    validator = BucketValidator()

    bucket = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('filename', filename)
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    validator.validate(bucket, cfg)

    assert sorted(validator.errors) == sorted(expected)


def test_bucket_duplicate_name(config_file):
    """The same name twice in one run is a duplicate.

    Uniqueness state belongs to the config, so both entities must be
    validated against the same one.
    """
    type_ = 'bucket'
    validator = BucketValidator()
    cfg = get_config(config_file)
    cfg.update('filename', 'bucket005_bucket.yml')
    cfg.update('skip_group_check', True)
    cfg.update('skip_service_account_check', True)

    test_input = {
        'name': 'bucket005',
        'team': 'team',
        'labels': {'app1': 'set'},
    }

    validator.validate(get_entity(type_)(**test_input), cfg)
    validator.clear()

    validator.validate(get_entity(type_)(**test_input), cfg)
    assert (
        "A duplicate object with name 'bucket005' already exists"
        in validator.errors
    )


def test_bucket_wrong_member_entity(config_file):
    type_ = 'bucket'
    validator = BucketValidator()
    cfg = get_config(config_file)

    test_input, filename, expected = (
        # invalid bucket invalid member in permissions
        {
            'name': 'bucket007',
            'team': '',
            'labels': {'app1': 'not-set'},
            'permissions': {
                'bucketAdmin': [
                    'notallowed:123@example.com',
                ],
            },
        },
        # filename
        'bucket007_bucket.yml',
        # validation result
        [
            "'team' must be set",
            "'notallowed' is not allowed in 'bucketAdmin', "
            f'must be {sorted(cfg.allowed_types)}',
        ],
    )

    bucket = get_entity(type_)(**test_input)
    cfg.update('filename', filename)

    validator.validate(bucket, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()
