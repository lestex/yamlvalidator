from unittest.mock import Mock
from unittest.mock import mock_open
from unittest.mock import patch

import yaml

from src.lib.cache import FileCache

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


def test_save_data():
    with patch('builtins.open', mock_open()) as file:
        # Mock load_data to prevent it from opening the file during initialization
        with patch.object(FileCache, 'load_data', Mock()):
            cache = FileCache('test_path')
            cache.cache = mock_data
            cache.save_data()

        file.assert_called_once_with('test_path', 'w')


def test_get():
    with patch.object(FileCache, 'load_data', Mock()):
        cache = FileCache('test_path')

        cache.cache = {'key': {'exist': True}}

        # Test for existing, non-expired key
        assert cache.get('key') == {'exist': True}

        # Test for non-existing key
        assert cache.get('non_existing_key') is None


def test_put():
    with patch('builtins.open', mock_open(read_data='')):
        cache = FileCache('test_path')

        cache.put('new_key')
        assert 'new_key' in cache.cache
        assert cache.cache['new_key']['exist'] is True


def test_delete():
    with patch.object(FileCache, 'load_data', Mock()):
        cache = FileCache('test_path')
        cache.cache = {
            'key1': 'value1',
            'key2': 'value2',
        }

        cache.delete('key1')
        assert 'key1' not in cache.cache
        assert 'key2' in cache.cache

        # Delete non-existing key
        cache.delete('non_existing_key')  # Should not raise an error
        assert 'non_existing_key' not in cache.cache


def test_invalidate():
    with (
        patch.object(FileCache, 'load_data', Mock()),
        patch('builtins.open', mock_open()),
    ):
        cache = FileCache('test_path')
        cache.cache = {'key': 'value'}

        cache.invalidate()
        assert cache.cache == {}
