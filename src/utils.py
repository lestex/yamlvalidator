import os
from typing import Generator
from typing import Optional

import yaml


def read_file(filename: str) -> dict:
    """Reads a YAML file. An empty file gives an empty dict."""
    with open(filename) as f:
        return yaml.safe_load(f) or {}


def list_files(type_: str, path: Optional[str] = None) -> Generator:
    for file in os.scandir(path=path):
        if file.name.endswith(f'_{type_}.yml'):
            yield file.name
