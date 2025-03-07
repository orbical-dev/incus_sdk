"""
Images API client for Incus API.
"""

import os
import aiofiles
from typing import Dict, Any, List, Optional, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.image import Image


class ImagesAPI:
    """API client for Incus images."""

    def __init__(self, client: APIClient):
        """
        Initialize a new ImagesAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Image]:
        """
        List all images.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Image]: List of images.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/images", params=params)

        images = []
        for image_data in response.get("metadata", []):
            images.append(Image(client=self, **image_data))

        return images

    async def get(self, fingerprint: str) -> Image:
        """
        Get an image by fingerprint.

        Args:
            fingerprint: Fingerprint of the image.

        Returns:
            Image: The image.
        """
        response = await self.client.get(f"/1.0/images/{fingerprint}")
        return Image(client=self, **response.get("metadata", {}))

    async def create(
        self,
        image_data: bytes,
        filename: str = None,
        public: bool = False,
        auto_update: bool = False,
        properties: Dict[str, str] = None,
        wait: bool = False,
    ) -> Union[Dict[str, Any], Image]:
        """
        Create a new image.

        Args:
            image_data: Image data.
            filename: Name of the image file.
            public: Whether the image is public.
            auto_update: Whether the image auto-updates.
            properties: Image properties.
            wait: Whether to wait for the operation to complete.

        Returns:
            Union[Dict[str, Any], Image]: The operation response or the created image.
        """
        headers = {}
        if filename:
            headers["X-Incus-Filename"] = filename

        params = {}
        if public:
            params["public"] = "1"
        if auto_update:
            params["auto_update"] = "1"
        if properties:
            for key, value in properties.items():
                params[f"properties.{key}"] = value

        response = await self.client.post(
            "/1.0/images", data=image_data, params=params, headers=headers
        )

        if wait and "id" in response.get("metadata", {}):
            await self.client.wait_for_operation(response["metadata"]["id"])
            # Get the fingerprint from the operation metadata
            operation = await self.client.get(
                f"/1.0/operations/{response['metadata']['id']}"
            )
            fingerprint = operation.get("metadata", {}).get("fingerprint")
            if fingerprint:
                return await self.get(fingerprint)

        return response

    async def delete(self, fingerprint: str, wait: bool = False) -> Dict[str, Any]:
        """
        Delete an image.

        Args:
            fingerprint: Fingerprint of the image.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        response = await self.client.delete(f"/1.0/images/{fingerprint}")

        if wait and "id" in response.get("metadata", {}):
            return await self.client.wait_for_operation(response["metadata"]["id"])

        return response

    async def update(
        self, fingerprint: str, properties: Dict[str, Any], wait: bool = False
    ) -> Dict[str, Any]:
        """
        Update an image.

        Args:
            fingerprint: Fingerprint of the image.
            properties: New properties.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        response = await self.client.patch(
            f"/1.0/images/{fingerprint}", data=properties
        )

        if wait and "id" in response.get("metadata", {}):
            return await self.client.wait_for_operation(response["metadata"]["id"])

        return response

    async def export(self, fingerprint: str, target_path: str) -> None:
        """
        Export an image to a file.

        Args:
            fingerprint: Fingerprint of the image.
            target_path: Path to save the exported image.
        """
        response = await self.client.get(f"/1.0/images/{fingerprint}/export")

        async with aiofiles.open(target_path, "wb") as f:
            await f.write(response)

    async def create_alias(
        self, name: str, target: str, description: str = None
    ) -> Dict[str, Any]:
        """
        Create an image alias.

        Args:
            name: Name of the alias.
            target: Target fingerprint.
            description: Description of the alias.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"name": name, "target": target}

        if description:
            data["description"] = description

        return await self.client.post("/1.0/images/aliases", data=data)

    async def delete_alias(self, name: str) -> Dict[str, Any]:
        """
        Delete an image alias.

        Args:
            name: Name of the alias.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/images/aliases/{name}")

    async def get_alias(self, name: str) -> Dict[str, Any]:
        """
        Get an image alias.

        Args:
            name: Name of the alias.

        Returns:
            Dict[str, Any]: The alias.
        """
        return await self.client.get(f"/1.0/images/aliases/{name}")

    async def update_alias(
        self, name: str, target: str = None, description: str = None
    ) -> Dict[str, Any]:
        """
        Update an image alias.

        Args:
            name: Name of the alias.
            target: New target fingerprint.
            description: New description.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {}

        if target:
            data["target"] = target
        if description:
            data["description"] = description

        return await self.client.patch(f"/1.0/images/aliases/{name}", data=data)
