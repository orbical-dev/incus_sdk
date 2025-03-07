"""
Cluster API client for Incus API.
"""

from typing import Dict, Any, List, Optional, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.cluster import Cluster, ClusterMember


class ClusterAPI:
    """API client for Incus cluster."""

    def __init__(self, client: APIClient):
        """
        Initialize a new ClusterAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def get(self) -> Cluster:
        """
        Get cluster information.

        Returns:
            Cluster: The cluster.
        """
        response = await self.client.get("/1.0/cluster")
        return Cluster(client=self, **response.get("metadata", {}))

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update cluster configuration.

        Args:
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put("/1.0/cluster", data=config)

    async def list_members(self, recursion: int = 1) -> List[ClusterMember]:
        """
        List all cluster members.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[ClusterMember]: List of cluster members.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/cluster/members", params=params)

        members = []
        for member_data in response.get("metadata", []):
            members.append(ClusterMember(client=self, **member_data))

        return members

    async def get_member(self, name: str) -> ClusterMember:
        """
        Get a cluster member by name.

        Args:
            name: Name of the cluster member.

        Returns:
            ClusterMember: The cluster member.
        """
        response = await self.client.get(f"/1.0/cluster/members/{name}")
        return ClusterMember(client=self, **response.get("metadata", {}))

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
        data = {"server_name": name, "server_address": url}

        if config:
            data["config"] = config

        return await self.client.post("/1.0/cluster/members", data=data)

    async def update_member(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a cluster member.

        Args:
            name: Name of the cluster member.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(f"/1.0/cluster/members/{name}", data=config)

    async def delete_member(self, name: str) -> Dict[str, Any]:
        """
        Delete a cluster member.

        Args:
            name: Name of the cluster member.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/cluster/members/{name}")

    async def rename_member(self, name: str, new_name: str) -> Dict[str, Any]:
        """
        Rename a cluster member.

        Args:
            name: Current name of the cluster member.
            new_name: New name for the cluster member.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"server_name": new_name}

        return await self.client.post(f"/1.0/cluster/members/{name}", data=data)
