from src.config import Config
from src.entities.service_account import ServiceAccount
from src.rules import _validate_description
from src.rules import _validate_display_name
from src.rules import _validate_fields
from src.rules import _validate_filename
from src.rules import _validate_unique
from src.rules.permissions import _validate_members_unique
from src.rules.permissions import _validate_permissions_members_list


def validate_service_account_id(
    sa: ServiceAccount, config: Config
) -> list[str]:
    """Validates service_account has common prefix
    or explicitly allowed without it"""
    errors: list[str] = []
    required = config.sa_id_substring
    if (
        required
        and sa.account_id
        and required not in sa.account_id
        and sa.account_id not in config.allowed_service_accounts
    ):
        errors.append(f"'account_id' is incorrect, must include {required!r}")
    return errors


def validate_disabled(sa: ServiceAccount, config: Config) -> list[str]:
    """Validates value of disabled is boolean"""
    errors: list[str] = []
    if sa.disabled and not isinstance(sa.disabled, bool):
        errors.append("value of 'disabled' is incorrect, must be boolean")
    return errors


def validate_filename(sa: ServiceAccount, config: Config) -> list[str]:
    """Validates service_account name present in the filename"""
    errors: list[str] = []
    if sa.account_id:
        name = sa.account_id
        errors.extend(_validate_filename(name, sa.class_name, config))
    return errors


def validate_unique(sa: ServiceAccount, config: Config) -> list[str]:
    """Validates service_account is unique"""
    return _validate_unique(sa.account_id, config)


def validate_fields(sa: ServiceAccount, config: Config) -> list[str]:
    """Validates service account fields are same as defined in dataclass"""
    fields = sa.to_dict()
    return _validate_fields(sa.class_name, sa.valid_fields, fields, config)


def validate_description(sa: ServiceAccount, config: Config) -> list[str]:
    """Validate service account description present"""
    return _validate_description(sa.description, config)


def validate_display_name(sa: ServiceAccount, config: Config) -> list[str]:
    """Validate service account display_name present"""
    return _validate_display_name(sa.display_name, config)


def validate_members_unique(sa: ServiceAccount, config: Config) -> list[str]:
    """Validates members in permissions are unique"""
    errors: list[str] = []
    errors.extend(
        _validate_members_unique(
            sa.serviceAccountUser, 'serviceAccountUser', config
        )
    )
    errors.extend(
        _validate_members_unique(
            sa.workloadIdentityUser,
            'workloadIdentityUser',
            config,
        )
    )
    return errors


def validate_permissions_members(
    sa: ServiceAccount, config: Config
) -> list[str]:
    """Validates service account permissions members"""
    errors: list[str] = []
    errors.extend(
        _validate_permissions_members_list(
            'serviceAccountUser',
            sa.serviceAccountUser,
            config,
        )
    )
    errors.extend(
        _validate_permissions_members_list(
            'workloadIdentityUser',
            sa.workloadIdentityUser,
            config,
        )
    )
    return errors
