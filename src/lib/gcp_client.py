from typing import Optional
from typing import Tuple

import google.auth
from googleapiclient.discovery import HttpError
from googleapiclient.discovery import build


class BindingException(Exception):
    pass


def create_credentials():
    """
    Creates a credentials object from Google Cloud API
    using the default credentials. Returns tuple with
    credentials object and project.
    """
    credentials, project = google.auth.default()
    return credentials, project


class GCPClient:
    """Create a GCP API client"""

    def __init__(self, credentials=None, project=None) -> None:
        """Creates basic client for GCP"""
        if not (credentials and project):
            default_credentials, default_project = create_credentials()
            credentials = credentials or default_credentials
            project = project or default_project
        self.credentials = credentials
        self.project = project

    def _create_service(self, api_name, api_version):
        """Creates a GCP Resource bound to a specific API and version"""
        return build(
            api_name,
            api_version,
            credentials=self.credentials,
            cache_discovery=False,
        )

    @property
    def iam(self):
        if not hasattr(self, '_iam'):
            self._iam = self._create_service('iam', 'v1')
        return self._iam

    @property
    def cloudresourcemanager(self):
        """Google Cloud Resource Manager client"""
        if not hasattr(self, '_cloudresourcemanager'):
            self._cloudresourcemanager = self._create_service(
                'cloudresourcemanager', 'v1'
            )
        return self._cloudresourcemanager

    def service_account_exists(self, sa_name: str) -> bool:
        # https://googleapis.github.io/google-api-python-client/docs/dyn/iam_v1.projects.serviceAccounts.html#get
        name = f'projects/-/serviceAccounts/{sa_name}'
        try:
            self.iam.projects().serviceAccounts().get(name=name).execute()
            return True
        except HttpError as exc:
            if exc.resp['status'] == '404':
                return False

        return False

    # use the built-in role with least previleges to check the group bound
    # to it a good example of the role is: `roles/compute.imageUser`
    # 1. check the role exists (if not exist, put the warning message
    # and return from function)
    # 2. if role exists check if the group is already bound to iam role,
    # if True then exist, group exist in GCP, nothing else to do.
    # if False, check and remember the iam role's membership count
    # 3. bind the group to a role, if success - group exist, unbound and
    # return True
    # 4. if bind fails return False
    def group_exists(
        self,
        project_id: str,
        group_name: str,
        role_name: str,
    ) -> bool:
        """Returns True if the group exists in IAM."""
        count_before, bound = self.group_role_exists(
            project_id, group_name, role_name
        )

        # group already bound to a role return no errors
        if bound:
            return True

        # step 3, bind the group to a role
        try:
            self.bind_group_role(project_id, group_name, role_name)
        except HttpError:
            return False
        except Exception as e:
            raise BindingException(
                f'Group {group_name!r} failed to bind to {role_name!r}'
            ) from e

        # step 4, unbind the group from the role
        try:
            self.unbind_group_role(project_id, group_name, role_name)
        except Exception as e:
            raise BindingException(
                f'Group {group_name!r} failed to unbind to {role_name!r}'
            ) from e

        count_after, _ = self.group_role_exists(
            project_id, group_name, role_name
        )

        if count_before != count_after:
            raise BindingException(
                f'Group {group_name!r} failed to unbind to {role_name!r}'
            )

        return True

    def iam_role_exists(self, role_name: str) -> bool:
        """Returns True if the role exists in IAM."""
        try:
            self.iam.roles().get(name=role_name).execute()
            return True
        except HttpError as exc:
            if exc.resp['status'] == '404':
                return False

        return False

    def get_iam_policy(self, project_id: str, version: int = 1) -> dict:
        """Gets the current IAM policy dict for a given project."""
        policy = (
            self.cloudresourcemanager.projects()
            .getIamPolicy(
                resource=project_id,
                body={'options': {'requestedPolicyVersion': version}},
            )
            .execute()
        )
        return policy

    def set_iam_policy(self, project_id: str, policy: dict) -> dict:
        """Sets the IAM policy for a project."""
        policy = (
            self.cloudresourcemanager.projects()
            .setIamPolicy(resource=project_id, body={'policy': policy})
            .execute()
        )
        return policy

    def bind_group_role(
        self,
        project_id: str,
        group_name: str,
        role_name: str,
        policy: Optional[dict] = None,
    ) -> dict:
        """Binds a group to a role in the specified project."""
        member = 'group:{}'.format(group_name)
        policy = policy or self.get_iam_policy(project_id)
        binding = self.get_policy_role_binding(policy, role_name)
        if binding:
            if member in binding['members']:
                # Do nothing if the group is already a member of the role.
                # TODO: Do something else? Exception, return True/False?
                return policy
            binding['members'].append(member)
        else:
            if not self.iam_role_exists(role_name):
                raise Exception('Unknown role')
            binding = {'role': role_name, 'members': [member]}
            policy['bindings'].append(binding)
        policy = self.set_iam_policy(project_id, policy)
        return policy

    def unbind_group_role(
        self, project_id, group_name, role_name, policy=None
    ):
        """Unbinds a group from a role in the specified project
        Args:
            project_id: GCP project id.
            group_name: Group to unbind from the role.(email: name@org.com)
            role_name: GCP IAM role name.
        Returns:
            IAM policy dict.
        """
        member = 'group:{}'.format(group_name)
        policy = policy or self.get_iam_policy(project_id)
        binding = self.get_policy_role_binding(policy, role_name)
        if not binding:
            # Do nothing if the group is not a member of the role.
            # TODO: Do something else? Exception, return True/False?
            return policy
        if member in binding['members']:
            binding['members'].remove(member)
            policy = self.set_iam_policy(project_id, policy)
        return policy

    def group_role_exists(
        self,
        project_id: str,
        group_name: str,
        role_name: str,
        policy: Optional[dict] = None,
    ) -> Tuple[int, bool]:
        """Returns number of members for an iam binding
        if a binding exists between the group and
        role in the specified project."""
        member = group_name
        if 'group:' not in group_name:
            member = 'group:{}'.format(group_name)
        policy = policy or self.get_iam_policy(project_id)
        binding = self.get_policy_role_binding(policy, role_name)
        if not binding:
            return 0, False
        exist = member in binding['members']
        return len(binding['members']), exist

    def get_policy_role_binding(
        self, policy: dict, role_name: str
    ) -> Optional[dict]:
        """Returns the binding dict from the given policy
        for the given role_name."""
        for obj in policy['bindings']:
            if obj['role'] == role_name:
                return obj
        return None
