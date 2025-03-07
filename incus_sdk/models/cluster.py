"""
Cluster model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class ClusterMember(Model):
    """Model representing an Incus cluster member."""

    def __init__(
        self,
        client=None,
        server_name: str = None,
        url: str = None,
        database: bool = None,
        status: str = None,
        message: str = None,
        architecture: str = None,
        failure_domain: str = None,
        description: str = None,
        config: Dict[str, str] = None,
        roles: List[str] = None,
        **kwargs,
    ):
        """
        Initialize a new ClusterMember model.

        Args:
            client: The Incus client instance.
            server_name: Name of the cluster member.
            url: URL of the cluster member.
            database: Whether the member is a database node.
            status: Current status of the cluster member.
            message: Status message.
            architecture: Architecture of the cluster member.
            failure_domain: Failure domain of the cluster member.
            description: Description of the cluster member.
            config: Member configuration.
            roles: Roles of the cluster member.
            **kwargs: Additional attributes to set on the model.
        """
        self.server_name = server_name
        self.url = url
        self.database = database
        self.status = status
        self.message = message
        self.architecture = architecture
        self.failure_domain = failure_domain
        self.description = description
        self.config = config or {}
        self.roles = roles or []
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the cluster member."""
        return f"<ClusterMember: {self.server_name}>"

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the cluster member configuration.

        Args:
            config: The new configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.cluster.update_member(self.server_name, config)

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the cluster member.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.cluster.delete_member(self.server_name)


class Cluster(Model):
    """Model representing an Incus cluster."""

    def __init__(
        self,
        client=None,
        enabled: bool = None,
        member_config: List[Dict[str, Any]] = None,
        members: List[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a new Cluster model.

        Args:
            client: The Incus client instance.
            enabled: Whether clustering is enabled.
            member_config: Configuration for cluster members.
            members: List of cluster members.
            **kwargs: Additional attributes to set on the model.
        """
        self.enabled = enabled
        self.member_config = member_config or []
        self.members = [
            ClusterMember(client=client, **member) for member in (members or [])
        ]
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the cluster."""
        return f"<Cluster: {len(self.members)} members>"

    async def get_member(self, name: str) -> ClusterMember:
        """
        Get a cluster member by name.

        Args:
            name: Name of the cluster member.

        Returns:
            ClusterMember: The cluster member.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.cluster.get_member(name)

    async def add_member(
        self, name: str, url: str, config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Add a new member to the cluster.

        Args:
            name: Name of the cluster member.
            url: URL of the cluster member.
            config: Member configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.cluster.add_member(name, url, config)
