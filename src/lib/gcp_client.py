import google.auth
from googleapiclient.discovery import HttpError
from googleapiclient.discovery import build


def create_credentials():
    """
    Creates a credentials object from Google Cloud API
    using the default credentials. Returns tuple with
    credentials object and project.
    """
    credentials, project = google.auth.default()
    return credentials, project


class GCPClient:
    """Create a GCP API client"""

    def __init__(self, credentials=None, project=None) -> None:
        """Creates basic client for GCP"""
        if not (credentials and project):
            default_credentials, default_project = create_credentials()
            credentials = credentials or default_credentials
            project = project or default_project
        self.credentials = credentials
        self.project = project

    def _create_service(self, api_name, api_version):
        """Creates a GCP Resource bound to a specific API and version"""
        return build(
            api_name,
            api_version,
            credentials=self.credentials,
            cache_discovery=False,
        )

    @property
    def iam(self):
        if not hasattr(self, '_iam'):
            self._iam = self._create_service('iam', 'v1')
        return self._iam

    def service_account_exists(self, sa_name: str) -> bool:
        # https://googleapis.github.io/google-api-python-client/docs/dyn/iam_v1.projects.serviceAccounts.html#get
        name = f'projects/-/serviceAccounts/{sa_name}'
        try:
            self.iam.projects().serviceAccounts().get(name=name).execute()
            return True
        except HttpError as exc:
            if exc.resp['status'] == '404':
                return False

        return False
