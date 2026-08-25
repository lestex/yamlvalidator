from unittest.mock import Mock

from src.lib.cache import cache_manager


def test_cache_manager_exists(cache_manager, gcp_client):
    gcp_client.group_exists.return_value = True
    assert cache_manager.exists('test_group') is True
    gcp_client.group_exists.assert_called_once_with(
        'test_project', 'test_group', 'test_role'
    )


def test_cache_manager_cached(cache_manager, cache):
    ret_val = cache.get.return_value = {'data': 'value'}
    assert cache_manager.cached('test_group') == ret_val
    cache.get.assert_called_once_with('test_group')


def test_put(cache_manager, cache):
    cache_manager.put('test_group')
    cache.put.assert_called_once_with('test_group')


def test_save(cache_manager, cache):
    cache_manager.save()
    cache.save_data.assert_called_once()


def test_cache_manager():
    cache = Mock()
    client = Mock()
    project = 'test_project'
    role = 'test_role'

    with cache_manager(cache, client, project, role) as manager:
        assert manager.project == project
        assert manager.role == role
        assert manager.cache is cache
        assert manager.client is client

    cache.save_data.assert_called_once()
