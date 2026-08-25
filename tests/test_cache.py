from unittest.mock import Mock
from unittest.mock import mock_open
from unittest.mock import patch

import yaml

from yamlvalidator.lib.cache import FileCache

mock_data = {'key': {'exist': True}}


def test_file_cache_initialization():
    with patch('builtins.open', mock_open(read_data='')):
        cache = FileCache('test_path')
        assert cache.path == 'test_path'
        assert cache.cache == {}


def test_load_data():
    with patch('builtins.open', mock_open(read_data=yaml.dump(mock_data))):
        cache = FileCache('test_path')
        assert cache.cache == mock_data


def test_get():
    with patch.object(FileCache, 'load_data', Mock()):
        cache = FileCache('test_path')

        cache.cache = {'key': {'exist': True}}

        # Test for existing, non-expired key
        assert cache.get('key') == {'exist': True}

        # Test for non-existing key
        assert cache.get('non_existing_key') is None
