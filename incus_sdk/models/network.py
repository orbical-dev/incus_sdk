"""
Network model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class Network(Model):
    """Model representing an Incus network."""

    def __init__(
        self,
        client=None,
        name: str = None,
        description: str = None,
        type: str = None,
        config: Dict[str, str] = None,
        status: str = None,
        locations: List[str] = None,
        managed: bool = None,
        used_by: List[str] = None,
        project: str = None,
        **kwargs,
    ):
        """
        Initialize a new Network model.

        Args:
            client: The Incus client instance.
            name: Name of the network.
            description: Description of the network.
            type: Type of network.
            config: Network configuration.
            status: Current status of the network.
            locations: Locations where the network is available.
            managed: Whether the network is managed by Incus.
            used_by: List of resources using this network.
            project: Project the network belongs to.
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.description = description
        self.type = type
        self.config = config or {}
        self.status = status
        self.locations = locations or []
        self.managed = managed
        self.used_by = used_by or []
        self.project = project
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the network."""
        return f"<Network: {self.name}>"

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the network configuration.

        Args:
            config: The new configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.networks.update(self.name, config)

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the network.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.networks.delete(self.name)

    async def rename(self, new_name: str) -> Dict[str, Any]:
        """
        Rename the network.

        Args:
            new_name: The new name for the network.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.networks.rename(self.name, new_name)
