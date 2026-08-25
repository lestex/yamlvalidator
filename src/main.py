from pathlib import Path

import typer
from typing_extensions import Annotated

from src.config import Config
from src.config import get_config
from src.entities import get_entity
from src.entities import get_supported_entities
from src.errors import Errors
from src.utils import list_files
from src.utils import read_file
from src.validators import get_validator
from src.validators.base import BaseValidator

TYPES = ', '.join(get_supported_entities())


# the CLI application
app = typer.Typer()


# validators
def validate_type(value: str):
    """Validates resource type is correct"""
    if value not in get_supported_entities():
        raise typer.BadParameter(
            f'{value!r} is wrong, only any of: {TYPES!r} is allowed'
        )
    return value


def validate_path(value: Path):
    """Validates file path is correct"""
    if not value.is_file():
        raise typer.BadParameter(f'File: {str(value)!r} does not exist.')
    return value


def validate(validator: BaseValidator, type_: str, config: Config) -> Errors:
    errors = Errors()

    for filename in list_files(type_):
        objects = read_file(filename)

        for obj_name, obj in objects.items():
            entity = get_entity(type_)(**obj)
            config.update('filename', filename)
            config.update('obj_name', obj_name)

            validator.validate(entity, config)

            if validator.errors:
                entity_errors = validator.errors.copy()
                errors.add(obj_name, entity_errors)
                validator.clear()

    return errors


@app.command()
def main(
    type_: Annotated[
        str,
        typer.Option(
            '--type',
            callback=validate_type,
            help=f'Type of resource to validate: {TYPES}',
        ),
    ],
    config_file: Annotated[
        Path,
        typer.Option(
            '--config',
            callback=validate_path,
            help='Config file location',
        ),
    ] = Path('.yamlvalidator.yml'),
    skip_team_labels_check: Annotated[
        bool,
        typer.Option(
            '--skip-team-labels-check',
            help='skip team label check',
        ),
    ] = False,
    skip_group_check: Annotated[
        bool,
        typer.Option(
            '--skip-group-check',
            help='skip group check',
        ),
    ] = False,
    skip_service_account_check: Annotated[
        bool,
        typer.Option(
            '--skip-service-account-check',
            help='skip service account check',
        ),
    ] = False,
    show_config: Annotated[
        bool,
        typer.Option(
            '--show-config',
            help='Show config',
        ),
    ] = False,
    cache_file: Annotated[
        Path,
        typer.Option(
            '--cache-file',
            callback=validate_path,
            help='Cache file location',
        ),
    ] = Path('.membership_cache'),
):
    """Validate yml files for a specific resource type."""
    validator = get_validator(type_)
    config = get_config(str(config_file))

    # config file takes presedence over cli params
    if (
        config.skip_team_labels_check is None
        or config.skip_team_labels_check != skip_team_labels_check
    ):
        config.update('skip_team_labels_check', skip_team_labels_check)

    if (
        config.skip_group_check is None
        or config.skip_group_check != skip_group_check
    ):
        config.update('skip_group_check', skip_group_check)

    if (
        config.skip_service_account_check is None
        or config.skip_service_account_check != skip_service_account_check
    ):
        config.update('skip_service_account_check', skip_service_account_check)

    # pass valid cache file to a config object
    config.update('cache_file', str(cache_file))

    if show_config:
        print(config.to_json())

    errors = validate(validator, type_, config)

    if errors:
        print(errors)
        raise typer.Exit(code=1)
