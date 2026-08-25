from dataclasses import dataclass
from typing import Optional

from yamlvalidator.entities.base import BaseYamlEntity


@dataclass
class Key(BaseYamlEntity):
    """Class representation of key YAML.
    A subclass of `BaseYamlEntity` and thus includes a name.
    """

    keyring_name: Optional[str] = None
    key_purpose: Optional[str] = None
    key_rotation_period: Optional[str] = None
    is_version_template: Optional[bool] = None
    algorithm: Optional[str] = None
    protection_level: Optional[str] = None

    # permissions
    cryptoKeyDecrypter: Optional[list[str]] = None
    cryptoKeyEncrypter: Optional[list[str]] = None
    cryptoKeyEncrypterDecrypter: Optional[list[str]] = None
    importer: Optional[list[str]] = None
    keyAdmin: Optional[list[str]] = None
    publicKeyViewer: Optional[list[str]] = None
    signer: Optional[list[str]] = None
    signerVerifier: Optional[list[str]] = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def permission_types(self) -> list[str]:
        """Valid permissions type for key defined in terraform module"""
        return [
            'cryptoKeyDecrypter',
            'cryptoKeyEncrypter',
            'cryptoKeyEncrypterDecrypter',
            'importer',
            'keyAdmin',
            'publicKeyViewer',
            'signer',
            'signerVerifier',
        ]
