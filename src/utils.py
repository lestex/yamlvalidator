import os
from typing import Generator, Optional

import yaml


def read_file(filename: str) -> dict:
    with open(filename) as f:
        return yaml.safe_load(f)


def list_files(type_: str, path: Optional[str] = None) -> Generator:
    for file in os.scandir(path=path):
        if file.name.endswith(f'_{type_}.yml'):
            yield file.name
