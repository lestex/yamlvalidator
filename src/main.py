from pathlib import Path
from typing import Optional

import typer
import yaml
from typing_extensions import Annotated

from src.config import Config
from src.config import get_config
from src.entities import get_entity
from src.entities import get_supported_entities
from src.errors import Errors
from src.utils import NotAMappingError
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
        try:
            objects = read_file(filename)
        except (NotAMappingError, yaml.YAMLError) as exc:
            # a CI gate must name the offending file rather than
            # exit with a traceback
            errors.add(filename, [str(exc)])
            continue

        for obj_name, obj in objects.items():
            if not isinstance(obj, dict):
                errors.add(
                    obj_name,
                    [f'must be a mapping, found {type(obj).__name__}'],
                )
                continue

            entity = get_entity(type_)(**obj)
            config.update('filename', filename)
            config.update('obj_name', obj_name)

            validator.validate(entity, config)

            if validator.errors:
                errors.add(obj_name, validator.errors)
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
    # these default to None so that "not passed" stays distinguishable
    # from "passed false" and the config file can be left in charge
    skip_team_labels_check: Annotated[
        Optional[bool],
        typer.Option(
            '--skip-team-labels-check/--no-skip-team-labels-check',
            help='skip team label check; overrides the config file',
            show_default=False,
        ),
    ] = None,
    skip_group_check: Annotated[
        Optional[bool],
        typer.Option(
            '--skip-group-check/--no-skip-group-check',
            help='skip group check; overrides the config file',
            show_default=False,
        ),
    ] = None,
    skip_service_account_check: Annotated[
        Optional[bool],
        typer.Option(
            '--skip-service-account-check/--no-skip-service-account-check',
            help='skip service account check; overrides the config file',
            show_default=False,
        ),
    ] = None,
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
    try:
        config = get_config(str(config_file))
    except (NotAMappingError, yaml.YAMLError) as exc:
        raise typer.BadParameter(str(exc), param_hint='--config') from exc

    # a cli flag takes precedence when it is passed, otherwise the value
    # from the config file (or its default) stands
    cli_flags = {
        'skip_team_labels_check': skip_team_labels_check,
        'skip_group_check': skip_group_check,
        'skip_service_account_check': skip_service_account_check,
    }
    for flag, value in cli_flags.items():
        if value is not None:
            config.update(flag, value)

    # pass valid cache file to a config object
    config.update('cache_file', str(cache_file))

    if show_config:
        print(config.to_json())

    errors = validate(validator, type_, config)

    if errors:
        print(errors)
        raise typer.Exit(code=1)
