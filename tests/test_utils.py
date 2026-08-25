import importlib

from src.entities import get_supported_entities
from src.utils import read_file


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


def test_read_file_empty(tmp_path):
    """An empty yml file must not blow up the caller."""
    empty = tmp_path / 'empty_bucket.yml'
    empty.write_text('')

    assert read_file(str(empty)) == {}
