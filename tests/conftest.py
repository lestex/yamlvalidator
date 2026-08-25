import os

import pytest
import yaml


@pytest.fixture
def config_obj():
    return {
        'allowed_user_emails': [],
        'allowed_service_accounts': [],
        'allowed_group_domains': ['example.com'],
        'allowed_user_domains': ['partner.example.com'],
        'sa_project_prefix': 'my-org-',
        'sa_id_substring': 'pl-',
        'allowed_types': [
            'user',
            'serviceAccount',
            'group',
        ],
    }


@pytest.fixture
def config_file(pytestconfig, config_obj):
    path = os.path.join(pytestconfig.rootpath, '.config.yml')
    with open(path, 'w') as file:
        yaml.dump(config_obj, file)

    yield path
    os.remove(path)


@pytest.fixture
def config_file_cli_params_set(pytestconfig, config_obj):
    config_obj['skip_team_labels_check'] = False
    config_obj['skip_group_check'] = False
    path = os.path.join(pytestconfig.rootpath, '.config.yml')
    with open(path, 'w') as file:
        yaml.dump(config_obj, file)

    yield path
    os.remove(path)


@pytest.fixture
def config_file_skips_enabled(pytestconfig, config_obj):
    """A config file that turns the optional checks off on its own."""
    config_obj['skip_team_labels_check'] = True
    config_obj['skip_group_check'] = True
    config_obj['skip_service_account_check'] = True
    path = os.path.join(pytestconfig.rootpath, '.config.yml')
    with open(path, 'w') as file:
        yaml.dump(config_obj, file)

    yield path
    os.remove(path)


@pytest.fixture
def config_file_cli_params_not_set(pytestconfig, config_obj):
    path = os.path.join(pytestconfig.rootpath, '.config.yml')
    with open(path, 'w') as file:
        yaml.dump(config_obj, file)

    yield path
    os.remove(path)


@pytest.fixture
def invalid_bucket_object() -> tuple:
    return {
        'testbucket:': {
            'name': 'testbucket',
            'team': '',
            'labels': {'app1': 'not-set'},
        },
    }, 'testbucketq_bucket.yml'


@pytest.fixture
def invalid_bucket_file(pytestconfig, invalid_bucket_object):
    obj, file = invalid_bucket_object
    path = os.path.join(pytestconfig.rootpath, file)
    with open(path, 'w') as file:
        yaml.dump(obj, file)

    yield
    os.remove(path)


@pytest.fixture
def malformed_bucket_file(pytestconfig):
    """A resource file whose top level is a list, not a mapping."""
    path = os.path.join(pytestconfig.rootpath, 'malformed_bucket.yml')
    with open(path, 'w') as file:
        file.write('- one\n- two\n')

    yield path
    os.remove(path)


@pytest.fixture
def valid_role_object() -> tuple:
    return {
        'testbrowser': {
            'role': 'roles/testbrowser',
            'members': ['group:123@example.com'],
        }
    }, 'testbrowser_role.yml'


@pytest.fixture
def valid_role_file(pytestconfig, valid_role_object):
    obj, file = valid_role_object
    path = os.path.join(pytestconfig.rootpath, file)
    with open(path, 'w') as file:
        yaml.dump(obj, file)

    yield
    os.remove(path)


@pytest.fixture
def membership_cache(pytestconfig):
    """The CLI validates --cache-file eagerly, so the default path must exist."""
    path = os.path.join(pytestconfig.rootpath, '.membership_cache')
    with open(path, 'w'):
        pass

    yield path
    os.remove(path)
