import json
import re
from typing import Any
from typing import Optional

from src.utils import read_file

# a GCP service account email must match this pattern
GSA = re.compile(
    r'^[\w\-]{4,30}(|\.iam|\.google.com.iam)\.gserviceaccount\.com$'
)

# Defaults for every option that is not set in the config file.
# An empty domain/prefix list means "do not enforce this policy".
DEFAULTS: dict[str, Any] = {
    'allowed_types': ['user', 'serviceAccount', 'group'],
    'allowed_group_domains': [],
    'allowed_user_domains': [],
    'allowed_user_emails': [],
    'allowed_service_accounts': [],
    'sa_project_prefix': '',
    'sa_id_substring': '',
    'team_validation_url': None,
    'skip_team_labels_check': False,
    'skip_group_check': False,
    'skip_service_account_check': False,
}


class Config:
    def __init__(self, file: str, obj: Optional[dict] = None) -> None:
        self._data = read_file(file)
        if obj:
            self._data.update(obj)

    # this allows to construct the config object with any field
    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._data:
            return self._data[name]
        return DEFAULTS.get(name, None)

    def update(self, name: str, value: Any) -> None:
        self._data[name] = value

    def to_dict(self):
        return self._data

    def to_json(self):
        return json.dumps(self._data)


def get_config(file: str, obj: Optional[dict] = None) -> Config:
    return Config(file, obj)
