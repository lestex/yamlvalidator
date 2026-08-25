import os
from typing import Generator
from typing import Optional

import yaml


class NotAMappingError(ValueError):
    """A YAML file's top level is not a mapping of resources."""


def read_file(filename: str) -> dict:
    """Reads a YAML file. An empty file gives an empty dict.

    Raises:
        NotAMappingError: the file's top level is not a mapping.
    """
    with open(filename) as f:
        data = yaml.safe_load(f)

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise NotAMappingError(
            f'{filename} must contain a mapping of resources, '
            f'found {type(data).__name__}'
        )

    return data


def list_files(type_: str, path: Optional[str] = None) -> Generator:
    """Yields the names of this type's resource files in `path`.

    Directories are skipped: a directory named `x_bucket.yml` is not a
    resource file.
    """
    for file in os.scandir(path=path):
        if file.name.endswith(f'_{type_}.yml') and file.is_file():
            yield file.name
