"""
Networks API client for Incus API.
"""

from typing import Dict, Any, List, Optional, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.network import Network


class NetworksAPI:
    """API client for Incus networks."""

    def __init__(self, client: APIClient):
        """
        Initialize a new NetworksAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Network]:
        """
        List all networks.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Network]: List of networks.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/networks", params=params)

        networks = []
        for network_data in response.get("metadata", []):
            networks.append(Network(client=self, **network_data))

        return networks

    async def get(self, name: str) -> Network:
        """
        Get a network by name.

        Args:
            name: Name of the network.

        Returns:
            Network: The network.
        """
        response = await self.client.get(f"/1.0/networks/{name}")
        return Network(client=self, **response.get("metadata", {}))

    async def create(
        self,
        name: str,
        config: Dict[str, Any],
        description: str = None,
        type: str = "bridge",
    ) -> Dict[str, Any]:
        """
        Create a new network.

        Args:
            name: Name of the network.
            config: Network configuration.
            description: Description of the network.
            type: Type of network.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": name, "type": type, "config": config}

        if description:
            data["description"] = description

        return await self.client.post("/1.0/networks", data=data)

    async def update(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a network.

        Args:
            name: Name of the network.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(f"/1.0/networks/{name}", data=config)

    async def replace(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace a network configuration.

        Args:
            name: Name of the network.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put(f"/1.0/networks/{name}", data=config)

    async def delete(self, name: str) -> Dict[str, Any]:
        """
        Delete a network.

        Args:
            name: Name of the network.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/networks/{name}")

    async def rename(self, name: str, new_name: str) -> Dict[str, Any]:
        """
        Rename a network.

        Args:
            name: Current name of the network.
            new_name: New name for the network.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": new_name}

        return await self.client.post(f"/1.0/networks/{name}", data=data)

    async def state(self, name: str) -> Dict[str, Any]:
        """
        Get the state of a network.

        Args:
            name: Name of the network.

        Returns:
            Dict[str, Any]: The network state.
        """
        response = await self.client.get(f"/1.0/networks/{name}/state")
        return response.get("metadata", {})
