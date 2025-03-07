"""
Project model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class Project(Model):
    """Model representing an Incus project."""

    def __init__(
        self,
        client=None,
        name: str = None,
        description: str = None,
        config: Dict[str, str] = None,
        used_by: List[str] = None,
        **kwargs,
    ):
        """
        Initialize a new Project model.

        Args:
            client: The Incus client instance.
            name: Name of the project.
            description: Description of the project.
            config: Project configuration.
            used_by: List of resources using this project.
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.description = description
        self.config = config or {}
        self.used_by = used_by or []
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the project."""
        return f"<Project: {self.name}>"

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the project configuration.

        Args:
            config: The new configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.projects.update(self.name, config)

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the project.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.projects.delete(self.name)

    async def rename(self, new_name: str) -> Dict[str, Any]:
        """
        Rename the project.

        Args:
            new_name: The new name for the project.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.projects.rename(self.name, new_name)
