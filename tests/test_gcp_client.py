from unittest.mock import Mock
from unittest.mock import patch

import pytest
from googleapiclient.discovery import HttpError

from src.lib.gcp_client import GCPClient


@pytest.fixture
def mock_google_auth_default():
    with patch('google.auth.default') as mock:
        mock.return_value = (Mock(), 'project_id')
        yield mock


@pytest.fixture
def gcp_client(mock_google_auth_default):
    return GCPClient()


def test_initialization_with_default_credentials(gcp_client):
    assert gcp_client.credentials
    assert gcp_client.project == 'project_id'


@patch('src.lib.gcp_client.build')
def test_service_account_exists(mock_build, gcp_client):
    mock_service = Mock()
    mock_build.return_value = mock_service
    # Setup mock response
    mock_service.projects().serviceAccounts().get().execute.return_value = {
        'name': 'test-service-account'
    }

    assert gcp_client.service_account_exists('test-service-account')


def _http_error(status: str) -> HttpError:
    resp = Mock()
    resp.__getitem__ = lambda self, key: status
    resp.status = int(status)
    resp.reason = 'error'
    return HttpError(resp=resp, content=b'{}')


@patch('src.lib.gcp_client.build')
def test_service_account_exists_404_is_absence(mock_build, gcp_client):
    """A 404 is the one status that means "does not exist"."""
    mock_service = Mock()
    mock_build.return_value = mock_service
    mock_service.projects().serviceAccounts().get().execute.side_effect = (
        _http_error('404')
    )

    assert gcp_client.service_account_exists('test-service-account') is False


@patch('src.lib.gcp_client.build')
def test_service_account_exists_403_raises(mock_build, gcp_client):
    """A permissions error must not be reported as absence."""
    mock_service = Mock()
    mock_build.return_value = mock_service
    mock_service.projects().serviceAccounts().get().execute.side_effect = (
        _http_error('403')
    )

    with pytest.raises(HttpError):
        gcp_client.service_account_exists('test-service-account')
