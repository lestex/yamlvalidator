from typing import Optional

import requests

from src.config import Config

# a set to validate duplicates
duplicates: set[Optional[str]] = set()


# COMMON VALIDATION RULES
# are not supposed to be used directly
# use a wrapper function instead for a specific validator type
def _validate_name(name: Optional[str], config: Config) -> list[str]:
    """Validate name present"""
    errors = []
    if not name:
        errors.append('Name must be set')
    return errors


def _validate_team(team: Optional[str], config: Config) -> list[str]:
    """Validate object team present and team name is valid.

    The team name is only checked against a remote directory when
    `team_validation_url` is configured and the check is not skipped.
    """
    errors = []
    if not team:
        errors.append('Team must be set')
        return errors

    url = config.team_validation_url
    if config.skip_team_labels_check or not url:
        return errors

    try:
        response = requests.get(f'{url}{team}', timeout=10)
    except requests.RequestException as exc:
        errors.append(f'could not validate team {team!r}: {exc}')
        return errors

    if response.status_code != 200:
        errors.append(f'{team!r} is invalid team name')

    return errors


def _validate_category(category: Optional[str], config: Config) -> list[str]:
    """Validate object category present"""
    errors = []
    if not category:
        errors.append('Category must be set')
    return errors


def _validate_labels(
    labels: Optional[dict[str, str]], config: Config
) -> list[str]:
    """Validate object labels and app1 key present"""
    errors = []
    label = 'app1'
    if not labels or label not in labels.keys():
        errors.append(f'at least {label!r} label must be set')
    return errors


def _validate_unique(name: Optional[str], config: Config) -> list[str]:
    """Validates object is only present once in all files"""
    errors = []
    if name in duplicates:
        errors.append(f'A duplicate object with name {name!r} already exists')
    duplicates.add(name)
    return errors


def _check_filename(name: Optional[str], config: Config) -> bool:
    """Helper function should not be called as a validator function.
    Returns:
    True - if object's name match the team in filename.
    False - otherwise
    """
    filename = config.filename
    return True if filename and f'{name}_' in filename else False


def _validate_filename(
    name: Optional[str], class_name: str, config: Config
) -> list[str]:
    """Validates object created in the proper file"""
    errors = []
    right_file = _check_filename(name, config)
    if not right_file:
        errors.append(f'filename must be: {name}_{class_name}.yml')
    return errors


def _validate_fields(
    class_name: str, valid_fields: list[str], fields: dict, config: Config
) -> list[str]:
    """Validates object fields are same as defined in dataclass"""
    errors = []
    for key in fields.keys():
        if key not in valid_fields:
            errors.append(f'field:{key!r} is not supported for {class_name}')
    return errors


def _validate_description(
    description: Optional[str], config: Config
) -> list[str]:
    """Validate description present"""
    errors = []
    if description == '':
        errors.append("'description' must be set")
    return errors


def _validate_display_name(
    display_name: Optional[str], config: Config
) -> list[str]:
    """Validate display_name present"""
    errors = []
    if display_name == '':
        errors.append("'display_name' must be set")
    return errors
