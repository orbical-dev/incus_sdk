"""
Profile model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class Profile(Model):
    """Model representing an Incus profile."""

    def __init__(
        self,
        client=None,
        name: str = None,
        description: str = None,
        config: Dict[str, str] = None,
        devices: Dict[str, Dict[str, str]] = None,
        used_by: List[str] = None,
        project: str = None,
        **kwargs,
    ):
        """
        Initialize a new Profile model.

        Args:
            client: The Incus client instance.
            name: Name of the profile.
            description: Description of the profile.
            config: Profile configuration.
            devices: Profile devices.
            used_by: List of resources using this profile.
            project: Project the profile belongs to.
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.description = description
        self.config = config or {}
        self.devices = devices or {}
        self.used_by = used_by or []
        self.project = project
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the profile."""
        return f"<Profile: {self.name}>"

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the profile configuration.

        Args:
            config: The new configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.profiles.update(self.name, config)

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the profile.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.profiles.delete(self.name)

    async def rename(self, new_name: str) -> Dict[str, Any]:
        """
        Rename the profile.

        Args:
            new_name: The new name for the profile.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.profiles.rename(self.name, new_name)
