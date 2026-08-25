import re

from yamlvalidator.config import Config
from yamlvalidator.entities.key import Key
from yamlvalidator.rules import _validate_fields
from yamlvalidator.rules import _validate_filename
from yamlvalidator.rules import _validate_unique
from yamlvalidator.rules.permissions import _validate_members_unique
from yamlvalidator.rules.permissions import _validate_permissions_members_list

ROTATION_REGEX = re.compile('^\\d{1,9}s$')

# a key must not rotate more often than once a day
MIN_ROTATION_PERIOD_SECONDS = 86400


VALID_KEYPURPOSE = [
    'CRYPTO_KEY_PURPOSE_UNSPECIFIED',
    'ENCRYPT_DECRYPT',
    'ASYMMETRIC_SIGN',
    'ASYMMETRIC_DECRYPT',
    'MAC',
]


VALID_KEYALGORITHM = [
    'CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED',
    'GOOGLE_SYMMETRIC_ENCRYPTION',
    'RSA_SIGN_PSS_2048_SHA256',
    'RSA_SIGN_PSS_3072_SHA256',
    'RSA_SIGN_PSS_4096_SHA256',
    'RSA_SIGN_PSS_4096_SHA512',
    'RSA_SIGN_PKCS1_2048_SHA256 ',
    'RSA_SIGN_PKCS1_3072_SHA256 ',
    'RSA_SIGN_PKCS1_4096_SHA256 ',
    'RSA_SIGN_PKCS1_4096_SHA512 ',
    'RSA_SIGN_RAW_PKCS1_2048',
    'RSA_SIGN_RAW_PKCS1_3072',
    'RSA_SIGN_RAW_PKCS1_4096',
    'RSA_DECRYPT_OAEP_2048_SHA256',
    'RSA_DECRYPT_OAEP_3072_SHA256',
    'RSA_DECRYPT_OAEP_4096_SHA256',
    'RSA_DECRYPT_OAEP_4096_SHA512',
    'RSA_DECRYPT_OAEP_2048_SHA1',
    'RSA_DECRYPT_OAEP_3072_SHA1',
    'RSA_DECRYPT_OAEP_4096_SHA1',
    'EC_SIGN_P256_SHA256',
    'EC_SIGN_P384_SHA384',
    'EC_SIGN_SECP256K1_SHA256',
    'HMAC_SHA256',
    'HMAC_SHA1',
    'HMAC_SHA384',
    'HMAC_SHA512',
    'HMAC_SHA224',
    'EXTERNAL_SYMMETRIC_ENCRYPTION',
]


VALID_PROTECTION_LEVELS = [
    'SOFTWARE',
    'HSM',
    'EXTERNAL',
    'EXTERNAL_VPC',
]


def validate_unique(key: Key, config: Config) -> list[str]:
    """Validates key is unique"""
    return _validate_unique(key.name, config)


def validate_fields(key: Key, config: Config) -> list[str]:
    """Validates key has only allowed fields"""
    fields = key.to_dict()
    return _validate_fields(key.class_name, key.valid_fields, fields, config)


def validate_filename(key: Key, config: Config) -> list[str]:
    """Validates key created in the right file"""
    return _validate_filename(key.name, key.class_name, config)


def validate_key_rotation_period(key: Key, config: Config) -> list[str]:
    """Validates key key_rotation_period"""
    errors = []
    if key.key_rotation_period:
        if re.fullmatch(ROTATION_REGEX, key.key_rotation_period):
            rotation = key.key_rotation_period.split('s')[0]
            if int(rotation) < MIN_ROTATION_PERIOD_SECONDS:
                errors.append(
                    "'key_rotation_period' must be at least "
                    f'{MIN_ROTATION_PERIOD_SECONDS} seconds'
                )
        else:
            errors.append(
                "'key_rotation_period' must be a decimal number with up "
                "to 9 digits, followed by the letter 's'"
            )

    return errors


def validate_members_unique(key: Key, config: Config) -> list[str]:
    """Validates key permissions members are unique"""
    errors = []
    permissions = key.permission_types

    for permission in permissions:
        key_perm_attr = getattr(key, permission)
        if key_perm_attr:
            errors.extend(
                _validate_members_unique(key_perm_attr, permission, config)
            )

    return errors


def validate_permissions_members(key: Key, config: Config) -> list[str]:
    """Validates key permissions members"""
    errors = []
    permissions = key.permission_types

    for permission in permissions:
        key_perm_attr = getattr(key, permission)
        if key_perm_attr:
            errors.extend(
                _validate_permissions_members_list(
                    permission, key_perm_attr, config
                )
            )

    return errors


def validate_key_purpose(key: Key, config: Config) -> list[str]:
    """Validates key purpose"""
    errors = []
    if key.key_purpose:
        if key.key_purpose not in VALID_KEYPURPOSE:
            errors.append(
                f'invalid key purpose set, must be one of: {VALID_KEYPURPOSE}'
            )
    return errors


def validate_is_version_template(key: Key, config: Config) -> list[str]:
    """Validates key is_validate_version_template properly set"""
    errors = []
    if key.is_version_template:
        if not key.algorithm or not key.protection_level:
            errors.append(
                "'algorithm' and 'protection_level' must be set "
                "when 'is_version_template' is set"
            )

    if key.algorithm:
        errors.extend(_validate_algorithm(key))

    if key.protection_level:
        errors.extend(_validate_protection_level(key))

    return errors


def _validate_algorithm(key: Key) -> list[str]:
    errors = []
    if key.algorithm not in VALID_KEYALGORITHM:
        errors.append(
            "invalid 'algorithm' set, see "
            "'https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm'"  # noqa
        )
    if not key.is_version_template:
        errors.append(
            "'is_version_template' must be also set when 'algorithm' is set"
        )
    return errors


def _validate_protection_level(key: Key) -> list[str]:
    errors = []
    if key.protection_level not in VALID_PROTECTION_LEVELS:
        errors.append(
            "invalid 'protection_level' set, must "
            f'be one of: {VALID_PROTECTION_LEVELS}'
        )

    if not key.is_version_template:
        errors.append(
            "'is_version_template' must be also set "
            "when 'protection_level' is set"
        )
    return errors
