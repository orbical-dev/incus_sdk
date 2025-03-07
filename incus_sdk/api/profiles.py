"""
Profiles API client for Incus API.
"""

from typing import Dict, Any, List, Optional, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.profile import Profile


class ProfilesAPI:
    """API client for Incus profiles."""

    def __init__(self, client: APIClient):
        """
        Initialize a new ProfilesAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Profile]:
        """
        List all profiles.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Profile]: List of profiles.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/profiles", params=params)

        profiles = []
        for profile_data in response.get("metadata", []):
            profiles.append(Profile(client=self, **profile_data))

        return profiles

    async def get(self, name: str) -> Profile:
        """
        Get a profile by name.

        Args:
            name: Name of the profile.

        Returns:
            Profile: The profile.
        """
        response = await self.client.get(f"/1.0/profiles/{name}")
        return Profile(client=self, **response.get("metadata", {}))

    async def create(
        self,
        name: str,
        config: Dict[str, Any] = None,
        description: str = None,
        devices: Dict[str, Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new profile.

        Args:
            name: Name of the profile.
            config: Profile configuration.
            description: Description of the profile.
            devices: Profile devices.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": name}

        if config:
            data["config"] = config
        if description:
            data["description"] = description
        if devices:
            data["devices"] = devices

        return await self.client.post("/1.0/profiles", data=data)

    async def update(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a profile.

        Args:
            name: Name of the profile.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(f"/1.0/profiles/{name}", data=config)

    async def replace(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace a profile configuration.

        Args:
            name: Name of the profile.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put(f"/1.0/profiles/{name}", data=config)

    async def delete(self, name: str) -> Dict[str, Any]:
        """
        Delete a profile.

        Args:
            name: Name of the profile.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/profiles/{name}")

    async def rename(self, name: str, new_name: str) -> Dict[str, Any]:
        """
        Rename a profile.

        Args:
            name: Current name of the profile.
            new_name: New name for the profile.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": new_name}

        return await self.client.post(f"/1.0/profiles/{name}", data=data)
