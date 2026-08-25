import json

from src.config import get_config


def test_config(config_obj, config_file):
    cfg = get_config(config_file)

    assert cfg.to_dict() == config_obj
    assert sorted(json.dumps(config_obj)) == sorted(cfg.to_json())

    obj = {'test_setting': 'test'}
    cfg_with_obj = get_config(config_file, obj=obj)
    assert cfg_with_obj.test_setting == 'test'
