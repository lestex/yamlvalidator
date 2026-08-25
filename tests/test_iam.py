import pytest

from yamlvalidator.iam import Member

WORKLOAD_IDENTITY = 'my-org-kube-dev.svc.id.goog[rc/hello-container-ksa]'


@pytest.mark.parametrize(
    'raw,kind,identifier',
    [
        ('user:someone@example.com', 'user', 'someone@example.com'),
        ('group:team@example.com', 'group', 'team@example.com'),
        (
            'serviceAccount:sa@proj.iam.gserviceaccount.com',
            'serviceAccount',
            'sa@proj.iam.gserviceaccount.com',
        ),
        (
            f'serviceAccount:{WORKLOAD_IDENTITY}',
            'serviceAccount',
            WORKLOAD_IDENTITY,
        ),
    ],
)
def test_parse_well_formed(raw, kind, identifier):
    member = Member.parse(raw)

    assert member is not None
    assert member.kind == kind
    assert member.identifier == identifier
    assert member.raw == raw


@pytest.mark.parametrize(
    'raw',
    [
        'no-separator',
        '',
        ':missing-kind@example.com',
        'user:',
        # a second colon is not part of the grammar
        'user:a:b',
    ],
)
def test_parse_malformed_returns_none(raw):
    assert Member.parse(raw) is None


def test_domain_takes_the_last_at_sign():
    """Two '@' must yield a domain, not raise.

    A bare unpack here is what used to crash the whole run on input like
    serviceAccount:a@b@example.com.
    """
    member = Member.parse('serviceAccount:a@b@example.com')

    assert member.domain == 'example.com'
    assert not member.is_workload_identity


def test_workload_identity_has_no_domain_of_its_own():
    member = Member.parse(f'serviceAccount:{WORKLOAD_IDENTITY}')

    assert member.is_workload_identity
    assert member.domain == WORKLOAD_IDENTITY


@pytest.mark.parametrize(
    'identifier,expected',
    [
        ('sa@proj.iam.gserviceaccount.com', True),
        ('sa@proj.svc.gserviceaccount.com', False),
        ('someone@example.com', False),
        ('a@b@example.com', False),
    ],
)
def test_is_service_account_email(identifier, expected):
    member = Member(
        'serviceAccount', identifier, f'serviceAccount:{identifier}'
    )

    assert member.is_service_account_email is expected


def test_member_is_frozen():
    member = Member.parse('user:someone@example.com')

    with pytest.raises(AttributeError):
        member.kind = 'group'
