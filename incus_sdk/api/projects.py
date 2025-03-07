"""
Projects API client for Incus API.
"""

from typing import Dict, Any, List, Optional, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.project import Project


class ProjectsAPI:
    """API client for Incus projects."""

    def __init__(self, client: APIClient):
        """
        Initialize a new ProjectsAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Project]:
        """
        List all projects.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Project]: List of projects.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/projects", params=params)

        projects = []
        for project_data in response.get("metadata", []):
            projects.append(Project(client=self, **project_data))

        return projects

    async def get(self, name: str) -> Project:
        """
        Get a project by name.

        Args:
            name: Name of the project.

        Returns:
            Project: The project.
        """
        response = await self.client.get(f"/1.0/projects/{name}")
        return Project(client=self, **response.get("metadata", {}))

    async def create(
        self, name: str, config: Dict[str, Any] = None, description: str = None
    ) -> Dict[str, Any]:
        """
        Create a new project.

        Args:
            name: Name of the project.
            config: Project configuration.
            description: Description of the project.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": name}

        if config:
            data["config"] = config
        if description:
            data["description"] = description

        return await self.client.post("/1.0/projects", data=data)

    async def update(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a project.

        Args:
            name: Name of the project.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(f"/1.0/projects/{name}", data=config)

    async def replace(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace a project configuration.

        Args:
            name: Name of the project.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put(f"/1.0/projects/{name}", data=config)

    async def delete(self, name: str) -> Dict[str, Any]:
        """
        Delete a project.

        Args:
            name: Name of the project.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/projects/{name}")

    async def rename(self, name: str, new_name: str) -> Dict[str, Any]:
        """
        Rename a project.

        Args:
            name: Current name of the project.
            new_name: New name for the project.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": new_name}

        return await self.client.post(f"/1.0/projects/{name}", data=data)

    async def state(self, name: str) -> Dict[str, Any]:
        """
        Get the state of a project.

        Args:
            name: Name of the project.

        Returns:
            Dict[str, Any]: The project state.
        """
        response = await self.client.get(f"/1.0/projects/{name}/state")
        return response.get("metadata", {})
