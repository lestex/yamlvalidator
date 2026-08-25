import re
from dataclasses import dataclass
from typing import Optional

# a GCP service account email must match this pattern
GSA = re.compile(
    r'^[\w\-]{4,30}(|\.iam|\.google.com.iam)\.gserviceaccount\.com$'
)


@dataclass(frozen=True)
class Member:
    """One entry in a resource's permission list.

    An IAM member is `<kind>:<identifier>`, where the identifier is an
    email for a user, a group or a service account, or a workload
    identity of the form `project.svc.id.goog[namespace/ksa]`.

    The grammar is stated once, here. A rule that needs the kind, the
    domain or the bare identifier asks the member for it rather than
    splitting the string again.
    """

    kind: str
    identifier: str
    raw: str

    @classmethod
    def parse(cls, raw: str) -> Optional['Member']:
        """Parses a member string, or returns None if it is malformed."""
        parts = raw.split(':')
        if len(parts) != 2:
            return None

        kind, identifier = parts
        if not kind or not identifier:
            return None

        return cls(kind=kind, identifier=identifier, raw=raw)

    @property
    def is_workload_identity(self) -> bool:
        """Workload identity accounts carry no email, so no domain."""
        return '@' not in self.identifier

    @property
    def domain(self) -> str:
        """Everything after the last '@'.

        Splitting from the right means a second '@' lands in the local
        part rather than raising, so a malformed address is reported by
        the rules instead of crashing the run.
        """
        return self.identifier.rsplit('@', 1)[-1]

    @property
    def is_service_account_email(self) -> bool:
        """True when the domain is a GCP service account domain."""
        return bool(GSA.search(self.domain))
