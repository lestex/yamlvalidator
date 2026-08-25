import json
import os

import pytest
import yaml

from src.config import UnknownConfigKeyError
from src.config import get_config


def test_config(config_obj, config_file):
    cfg = get_config(config_file)

    assert cfg.to_dict() == config_obj
    assert sorted(json.dumps(config_obj)) == sorted(cfg.to_json())

    obj = {'test_setting': 'test'}
    cfg_with_obj = get_config(config_file, obj=obj)
    assert cfg_with_obj.test_setting == 'test'


def test_config_rejects_misspelled_key(tmp_path, config_obj):
    """A typo must fail loudly, not silently disable a check."""
    config_obj['skip_group_ceck'] = True
    path = os.path.join(tmp_path, 'typo.yml')
    with open(path, 'w') as file:
        yaml.dump(config_obj, file)

    with pytest.raises(UnknownConfigKeyError, match='skip_group_ceck'):
        get_config(path)
