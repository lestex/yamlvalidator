from unittest.mock import Mock
from unittest.mock import patch

import pytest

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

    # # Test handling of HttpError 404
    # mock_service.projects().serviceAccounts().get().execute.side_effect = HttpError(resp=Mock(status=404), content=b'Not Found')
    # assert not gcp_client.service_account_exists('test-service-account')
