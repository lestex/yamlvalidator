from unittest.mock import MagicMock
from unittest.mock import patch

from src.rules import _validate_team
from src.rules.permissions import _check_group_exists
from src.rules.permissions import _check_service_account_exists
from src.rules.permissions import _valid_sa_domain


# __init__.py functions
# _validate_team
@patch('src.rules.requests')
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


# _check_service_account_exists
class MockGCPClient:
    def service_account_exists(self, sa):
        return sa != 'nonexistent_sa'


def test_check_service_account_exists():
    yes = 'existent_sa'
    no = 'nonexistent_sa'

    with patch('src.rules.permissions.GCPClient', MockGCPClient):
        with patch(
            'src.rules.permissions._valid_sa_domain',
            MagicMock(return_value=True),
        ):
            errors = _check_service_account_exists(yes, sa_config)
            assert errors == []

            errors = _check_service_account_exists(no, sa_config)
            assert errors == [
                "'nonexistent_sa' doesn't exist in GCP, create it first"
            ]


# _check_group_exists
class MockFileCache:
    def __init__(self, cache_path: str):
        pass

    def get(self, group):
        return group != 'nonexistent_group'


def test_check_group_exists():
    with patch('src.rules.permissions.FileCache', MockFileCache):
        errors = _check_group_exists(
            'existing_group', MagicMock(cache_path='dummy_cache_path')
        )
        assert errors == []

    # Group doesn't exist
    with patch('src.rules.permissions.FileCache', MockFileCache):
        errors = _check_group_exists(
            'nonexistent_group', MagicMock(cache_path='dummy_cache_path')
        )
        assert errors == [
            "'nonexistent_group' doesn't exist in GCP, create it first or check it is in the cache"
        ]
