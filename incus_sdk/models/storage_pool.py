"""
Storage pool model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class StorageVolume(Model):
    """Model representing an Incus storage volume."""

    def __init__(
        self,
        client=None,
        name: str = None,
        type: str = None,
        config: Dict[str, str] = None,
        description: str = None,
        content_type: str = None,
        location: str = None,
        used_by: List[str] = None,
        pool: str = None,
        project: str = None,
        **kwargs,
    ):
        """
        Initialize a new StorageVolume model.

        Args:
            client: The Incus client instance.
            name: Name of the volume.
            type: Type of volume.
            config: Volume configuration.
            description: Description of the volume.
            content_type: Content type of the volume.
            location: Location of the volume.
            used_by: List of resources using this volume.
            pool: Storage pool the volume belongs to.
            project: Project the volume belongs to.
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.type = type
        self.config = config or {}
        self.description = description
        self.content_type = content_type
        self.location = location
        self.used_by = used_by or []
        self.pool = pool
        self.project = project
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the storage volume."""
        return f"<StorageVolume: {self.name} ({self.pool})>"

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the storage volume configuration.

        Args:
            config: The new configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.update_volume(
            self.pool, self.name, self.type, config
        )

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the storage volume.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.delete_volume(
            self.pool, self.name, self.type
        )

    async def rename(self, new_name: str) -> Dict[str, Any]:
        """
        Rename the storage volume.

        Args:
            new_name: The new name for the storage volume.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.rename_volume(
            self.pool, self.name, self.type, new_name
        )


class StoragePool(Model):
    """Model representing an Incus storage pool."""

    def __init__(
        self,
        client=None,
        name: str = None,
        driver: str = None,
        description: str = None,
        config: Dict[str, str] = None,
        status: str = None,
        locations: List[str] = None,
        used_by: List[str] = None,
        project: str = None,
        **kwargs,
    ):
        """
        Initialize a new StoragePool model.

        Args:
            client: The Incus client instance.
            name: Name of the storage pool.
            driver: Storage driver.
            description: Description of the storage pool.
            config: Storage pool configuration.
            status: Current status of the storage pool.
            locations: Locations where the storage pool is available.
            used_by: List of resources using this storage pool.
            project: Project the storage pool belongs to.
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.driver = driver
        self.description = description
        self.config = config or {}
        self.status = status
        self.locations = locations or []
        self.used_by = used_by or []
        self.project = project
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the storage pool."""
        return f"<StoragePool: {self.name} ({self.driver})>"

    async def update(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the storage pool configuration.

        Args:
            config: The new configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.update(self.name, config)

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the storage pool.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.delete(self.name)

    async def list_volumes(self, volume_type: str = None) -> List[StorageVolume]:
        """
        List volumes in the storage pool.

        Args:
            volume_type: Type of volumes to list.

        Returns:
            List[StorageVolume]: List of storage volumes.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.list_volumes(self.name, volume_type)

    async def create_volume(
        self, name: str, volume_type: str, config: Dict[str, Any] = None
    ) -> StorageVolume:
        """
        Create a new volume in the storage pool.

        Args:
            name: Name of the volume.
            volume_type: Type of volume.
            config: Volume configuration.

        Returns:
            StorageVolume: The created storage volume.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.storage_pools.create_volume(
            self.name, name, volume_type, config
        )
