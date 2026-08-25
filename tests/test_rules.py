from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from googleapiclient.discovery import HttpError

from yamlvalidator.config import get_config
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules import _validate_team
from yamlvalidator.rules.permissions import _check_group_exists
from yamlvalidator.rules.permissions import _check_member_service_account
from yamlvalidator.rules.permissions import _check_member_user
from yamlvalidator.rules.permissions import _check_service_account_exists
from yamlvalidator.rules.permissions import _valid_sa_domain


# __init__.py functions
# _validate_team
@patch('yamlvalidator.rules.requests')
def test_invalid_team_name(requests_mock):
    config_mock = MagicMock(skip_team_labels_check=False)
    response_mock = MagicMock(status_code=404)
    requests_mock.get.return_value = response_mock
    errors = _validate_team('invalid_team', config_mock)
    assert errors == ["'invalid_team' is invalid team name"]


# permissions.py functions
# _valid_sa_domain
sa_config = MagicMock(sa_project_prefix='my-org-')


def test_valid_sa_domain_invalid_domain():
    assert not _valid_sa_domain('user@invalid.com', sa_config)


def test_valid_sa_domain_no_divider():
    assert not _valid_sa_domain('username', sa_config)


def test_valid_sa_domain_empty_string():
    assert not _valid_sa_domain('', sa_config)


def test_valid_sa_domain_whitespace_string():
    assert not _valid_sa_domain('   ', sa_config)


# _validate_filename
def test_validate_filename_exact_match():
    config = MagicMock(filename='myname_bucket.yml')

    assert _validate_filename('myname', 'bucket', config) == []


def test_validate_filename_rejects_prefixed_name():
    """The check is an exact match, not a substring one."""
    config = MagicMock(filename='prefix_myname_bucket.yml')

    errors = _validate_filename('myname', 'bucket', config)

    assert errors == ['filename must be: myname_bucket.yml']


def test_validate_filename_rejects_wrong_type_suffix():
    """A bucket may not live in a file named for another type."""
    config = MagicMock(filename='myname_secret.yml')

    errors = _validate_filename('myname', 'bucket', config)

    assert errors == ['filename must be: myname_bucket.yml']


# _check_service_account_exists
class MockGCPClient:
    def service_account_exists(self, sa):
        return sa != 'nonexistent_sa'


def test_check_service_account_exists():
    yes = 'existent_sa'
    no = 'nonexistent_sa'

    with patch('yamlvalidator.rules.permissions.GCPClient', MockGCPClient):
        with patch(
            'yamlvalidator.rules.permissions._valid_sa_domain',
            MagicMock(return_value=True),
        ):
            errors = _check_service_account_exists(yes, sa_config)
            assert errors == []

            errors = _check_service_account_exists(no, sa_config)
            assert errors == [
                "'nonexistent_sa' doesn't exist in GCP, create it first"
            ]


class RaisingGCPClient:
    def service_account_exists(self, sa):
        resp = Mock()
        resp.__getitem__ = lambda self, key: '403'
        resp.status = 403
        resp.reason = 'Forbidden'
        raise HttpError(resp=resp, content=b'{}')


def test_check_service_account_api_error_is_not_absence():
    """A 403 must read as "could not verify", not "create it first"."""
    with patch('yamlvalidator.rules.permissions.GCPClient', RaisingGCPClient):
        with patch(
            'yamlvalidator.rules.permissions._valid_sa_domain',
            MagicMock(return_value=True),
        ):
            errors = _check_service_account_exists('some_sa', sa_config)

    assert len(errors) == 1
    assert errors[0].startswith("could not verify 'some_sa' in GCP")
    assert "doesn't exist" not in errors[0]


# _check_member_user
def test_check_member_user_no_allowed_domains():
    """With no domains allowed, the message must not read '[] allowed'."""
    config_mock = MagicMock(allowed_user_domains=[], allowed_user_emails=[])

    errors = _check_member_user('someone@example.com', config_mock)

    assert len(errors) == 1
    assert '[]' not in errors[0]
    assert 'only specific users are allowed' in errors[0]


# _check_member_service_account
def test_check_member_service_account_extra_at_sign():
    """An email with two '@' must be reported, not raise ValueError."""
    config_mock = MagicMock(skip_service_account_check=True)

    errors = _check_member_service_account('a@b@example.com', config_mock)

    assert errors == ['invalid Service Account']


# _check_group_exists
class MockFileCache:
    opened = 0

    def __init__(self, cache_path: str):
        MockFileCache.opened += 1

    def get(self, group):
        return group != 'nonexistent_group'


def test_check_group_exists():
    config = MagicMock(group_cache=MockFileCache('dummy_cache_path'))

    errors = _check_group_exists('existing_group', config)
    assert errors == []

    # Group doesn't exist
    errors = _check_group_exists('nonexistent_group', config)
    assert errors == [
        "'nonexistent_group' doesn't exist in GCP, create it first or check it is in the cache"
    ]


def test_group_cache_is_built_once(config_file):
    """The cache file is read once per run, not once per member."""
    cfg = get_config(config_file)
    cfg.update('cache_file', 'dummy_cache_path')

    MockFileCache.opened = 0
    with patch('yamlvalidator.config.FileCache', MockFileCache):
        for _ in range(50):
            _check_group_exists('a_group', cfg)

    assert MockFileCache.opened == 1
