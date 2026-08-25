import re
from typing import Optional
from typing import Union

from googleapiclient.discovery import HttpError

from src.config import GSA
from src.config import Config
from src.lib.gcp_client import GCPClient


# PERMISSIONS VALIDATION RULES
def _validate_permissions(
    valid_permissions: list[str],
    permissions: Optional[dict[str, list[str]]],
    config: Config,
) -> list[str]:
    """Validate object has proper permissions"""
    errors = []
    if permissions:
        for permission in permissions.keys():
            if permission not in valid_permissions:
                errors.append(
                    f'{permission!r} is not valid, must be {valid_permissions}'
                )
    return errors


def _validate_unique_list(
    permissions_list: list[str], property_name: str
) -> list[str]:
    duplicates = set()
    errors = []
    for member in permissions_list:
        if member in duplicates:
            errors.append(
                f'{property_name!r} has a duplicate member {member!r}'
            )
        duplicates.add(member)
    return errors


def _validate_unique_dict(
    permissions_dict: dict[str, list[str]], property_name: str
) -> list[str]:
    errors = []
    for permission, members in permissions_dict.items():
        duplicates = set()
        for member in members:
            if member in duplicates:
                errors.append(
                    f'{property_name!r}:{permission!r} has a '
                    f'duplicate member {member!r}'
                )
            duplicates.add(member)
    return errors


def _validate_members_unique(
    permissions: Union[Optional[list[str]], Optional[dict[str, list[str]]]],
    property_name: str,
    config: Config,
) -> list[str]:
    """Validates permissions members are unique"""
    errors = []
    if permissions and isinstance(permissions, list):
        errors.extend(_validate_unique_list(permissions, property_name))

    if permissions and isinstance(permissions, dict):
        errors.extend(_validate_unique_dict(permissions, property_name))
    return errors


def _check_member_type(perm: str, perm_type: str, config: Config) -> list[str]:
    errors = []
    if perm_type not in config.allowed_types:
        errors.append(
            f'{perm_type!r} is not allowed in {perm!r}, '
            f'must be {sorted(config.allowed_types)}'
        )
    return errors


def _check_member_group(email: str, config: Config) -> list[str]:
    errors = []
    domain = email.rsplit('@', 1)[-1]
    allowed = config.allowed_group_domains
    if allowed and domain not in allowed:
        errors.append(f'only groups from {sorted(allowed)} are allowed')

    # check group exist in GCP
    skip = config.skip_group_check
    if not skip:
        errors.extend(_check_group_exists(email, config))
    return errors


def _check_member_service_account(email: str, config: Config) -> list[str]:
    errors = []
    domain = email.rsplit('@', 1)[-1]
    if not GSA.search(domain):
        errors.append('invalid Service Account')

    # check service account exist in GCP
    skip = config.skip_service_account_check
    if not skip:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            errors.extend(_check_service_account_exists(email, config))
    return errors


def _check_member_user(email: str, config: Config) -> list[str]:
    errors = []
    domain = email.rsplit('@', 1)[-1]
    allowed_domains = config.allowed_user_domains
    if (
        domain not in allowed_domains
        and email not in config.allowed_user_emails
    ):
        if allowed_domains:
            errors.append(
                f'{email} must not be used here, only specific users or '
                f'users from {sorted(allowed_domains)} allowed, '
                "use 'group' instead"
            )
        else:
            # no domain is allowed, so naming the empty list helps nobody
            errors.append(
                f'{email} must not be used here, only specific users '
                "are allowed, use 'group' instead"
            )
    return errors


def _managed_sa_domain(domain: str, config: Config) -> bool:
    """True when the service account belongs to a project we manage."""
    return domain.startswith(config.sa_project_prefix)


def _valid_sa_domain(member: str, config: Config) -> bool:
    divider = '@'
    if divider in member:
        domain = member.rsplit(divider, 1)[-1]
        return _managed_sa_domain(domain, config)
    return False


def _check_service_account_exists(sa: str, config: Config) -> list[str]:
    errors: list[str] = []
    if not (re.match('[^/]+$', sa) and _valid_sa_domain(sa, config)):
        return errors

    client = GCPClient()
    try:
        exists = client.service_account_exists(sa)
    except HttpError as exc:
        # an api error is not evidence of absence: say so rather than
        # telling the developer to create an account that may exist
        errors.append(f'could not verify {sa!r} in GCP: {exc}')
        return errors

    if not exists:
        errors.append(f"{sa!r} doesn't exist in GCP, create it first")
    return errors


def _check_group_exists(group: str, config: Config) -> list[str]:
    errors: list[str] = []
    # check the `group` in the file cache, built once per run
    if not config.group_cache.get(group):
        errors.append(
            f"{group!r} doesn't exist in GCP, create "
            'it first or check it is in the cache'
        )
    return errors


def _check_type(member: str) -> tuple[Optional[str], Optional[str]]:
    try:
        grant_type, email = member.split(':')
        return grant_type, email
    except Exception:
        return None, None


# each member is any of:
# user:username@example.com
# group:groupname@example.com
# serviceAccount:sa@my-project.iam.gserviceaccount.com
# serviceAccount:my-project.svc.id.goog[namespace/some-ksa]
def _check_member(permission: str, member: str, config: Config) -> list[str]:
    errors = []
    member_type, email = _check_type(member)

    # cover all edge cases
    if not member_type or not email:
        errors.append(f'Invalid entity: {member}')
        return errors

    errors.extend(_check_member_type(permission, member_type, config))

    # workload identity service accounts have no '@' and need no further
    # checks beyond the member type
    if '@' in email:
        match member_type:
            case 'user':
                errors.extend(_check_member_user(email, config))
            case 'group':
                errors.extend(_check_member_group(email, config))
            case 'serviceAccount':
                errors.extend(_check_member_service_account(email, config))

    return errors


def _check_members(
    permission: str, members: list[str], config: Config
) -> list[str]:
    errors = []
    for member in members:
        errors.extend(_check_member(permission, member, config))
    return errors


# some resources have `permissions` property
def _validate_permissions_members_dict(
    permissions: Optional[dict[str, list[str]]], config: Config
) -> list[str]:
    """Validates the permissions property of a resource"""
    errors = []
    if permissions:
        for permission, members in permissions.items():
            errors.extend(_check_members(permission, members, config))

    return errors


# some resources have `members` property
def _validate_permissions_members_list(
    permission: str,
    members: Optional[list[str]],
    config: Config,
) -> list[str]:
    """Validates the members property of a resource"""
    errors = []
    if members:
        errors.extend(_check_members(permission, members, config))

    return errors
