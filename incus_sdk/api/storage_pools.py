"""
Storage pools API client for Incus API.
"""

from typing import Dict, Any, List, Optional, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.storage_pool import StoragePool, StorageVolume


class StoragePoolsAPI:
    """API client for Incus storage pools."""

    def __init__(self, client: APIClient):
        """
        Initialize a new StoragePoolsAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[StoragePool]:
        """
        List all storage pools.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[StoragePool]: List of storage pools.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/storage-pools", params=params)

        pools = []
        for pool_data in response.get("metadata", []):
            pools.append(StoragePool(client=self, **pool_data))

        return pools

    async def get(self, name: str) -> StoragePool:
        """
        Get a storage pool by name.

        Args:
            name: Name of the storage pool.

        Returns:
            StoragePool: The storage pool.
        """
        response = await self.client.get(f"/1.0/storage-pools/{name}")
        return StoragePool(client=self, **response.get("metadata", {}))

    async def create(
        self,
        name: str,
        driver: str,
        config: Dict[str, Any] = None,
        description: str = None,
    ) -> Dict[str, Any]:
        """
        Create a new storage pool.

        Args:
            name: Name of the storage pool.
            driver: Storage driver.
            config: Storage pool configuration.
            description: Description of the storage pool.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": name, "driver": driver}

        if config:
            data["config"] = config
        if description:
            data["description"] = description

        return await self.client.post("/1.0/storage-pools", data=data)

    async def update(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a storage pool.

        Args:
            name: Name of the storage pool.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(f"/1.0/storage-pools/{name}", data=config)

    async def replace(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace a storage pool configuration.

        Args:
            name: Name of the storage pool.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put(f"/1.0/storage-pools/{name}", data=config)

    async def delete(self, name: str) -> Dict[str, Any]:
        """
        Delete a storage pool.

        Args:
            name: Name of the storage pool.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/storage-pools/{name}")

    async def list_volumes(
        self, pool_name: str, volume_type: str = None, recursion: int = 1
    ) -> List[StorageVolume]:
        """
        List volumes in a storage pool.

        Args:
            pool_name: Name of the storage pool.
            volume_type: Type of volumes to list.
            recursion: Level of recursion for the response.

        Returns:
            List[StorageVolume]: List of storage volumes.
        """
        path = f"/1.0/storage-pools/{pool_name}/volumes"
        if volume_type:
            path = f"{path}/{volume_type}"

        params = {"recursion": recursion}
        response = await self.client.get(path, params=params)

        volumes = []
        for volume_data in response.get("metadata", []):
            volume_data["pool"] = pool_name
            volumes.append(StorageVolume(client=self, **volume_data))

        return volumes

    async def get_volume(
        self, pool_name: str, volume_name: str, volume_type: str
    ) -> StorageVolume:
        """
        Get a storage volume by name.

        Args:
            pool_name: Name of the storage pool.
            volume_name: Name of the volume.
            volume_type: Type of volume.

        Returns:
            StorageVolume: The storage volume.
        """
        response = await self.client.get(
            f"/1.0/storage-pools/{pool_name}/volumes/{volume_type}/{volume_name}"
        )
        volume_data = response.get("metadata", {})
        volume_data["pool"] = pool_name
        return StorageVolume(client=self, **volume_data)

    async def create_volume(
        self,
        pool_name: str,
        volume_name: str,
        volume_type: str,
        config: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Create a new storage volume.

        Args:
            pool_name: Name of the storage pool.
            volume_name: Name of the volume.
            volume_type: Type of volume.
            config: Volume configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": volume_name, "type": volume_type}

        if config:
            data["config"] = config

        return await self.client.post(
            f"/1.0/storage-pools/{pool_name}/volumes", data=data
        )

    async def update_volume(
        self, pool_name: str, volume_name: str, volume_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a storage volume.

        Args:
            pool_name: Name of the storage pool.
            volume_name: Name of the volume.
            volume_type: Type of volume.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(
            f"/1.0/storage-pools/{pool_name}/volumes/{volume_type}/{volume_name}",
            data=config,
        )

    async def replace_volume(
        self, pool_name: str, volume_name: str, volume_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Replace a storage volume configuration.

        Args:
            pool_name: Name of the storage pool.
            volume_name: Name of the volume.
            volume_type: Type of volume.
            config: New configuration.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put(
            f"/1.0/storage-pools/{pool_name}/volumes/{volume_type}/{volume_name}",
            data=config,
        )

    async def delete_volume(
        self, pool_name: str, volume_name: str, volume_type: str
    ) -> Dict[str, Any]:
        """
        Delete a storage volume.

        Args:
            pool_name: Name of the storage pool.
            volume_name: Name of the volume.
            volume_type: Type of volume.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(
            f"/1.0/storage-pools/{pool_name}/volumes/{volume_type}/{volume_name}"
        )

    async def rename_volume(
        self, pool_name: str, volume_name: str, volume_type: str, new_name: str
    ) -> Dict[str, Any]:
        """
        Rename a storage volume.

        Args:
            pool_name: Name of the storage pool.
            volume_name: Current name of the volume.
            volume_type: Type of volume.
            new_name: New name for the volume.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": new_name}

        return await self.client.post(
            f"/1.0/storage-pools/{pool_name}/volumes/{volume_type}/{volume_name}",
            data=data,
        )
