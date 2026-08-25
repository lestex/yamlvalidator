import importlib

from src.entities import get_supported_entities


def test_get_supported_entities_method():
    modules = importlib.import_module('src.entities')
    right = sorted(
        [
            'bqdataset',
            'bqtable',
            'bucket',
            'key',
            'keyring',
            'role',
            'sa',
            'secret',
            'service',
        ]
    )

    modules = get_supported_entities()
    assert modules == right
