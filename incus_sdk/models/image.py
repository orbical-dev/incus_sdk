"""
Image model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class ImageAlias(Model):
    """Model representing an Incus image alias."""

    def __init__(
        self, client=None, name: str = None, description: str = None, **kwargs
    ):
        """
        Initialize a new ImageAlias model.

        Args:
            client: The Incus client instance.
            name: Name of the alias.
            description: Description of the alias.
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.description = description
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the image alias."""
        return f"<ImageAlias: {self.name}>"


class Image(Model):
    """Model representing an Incus image."""

    def __init__(
        self,
        client=None,
        fingerprint: str = None,
        filename: str = None,
        size: int = None,
        architecture: str = None,
        created_at: str = None,
        expires_at: str = None,
        uploaded_at: str = None,
        last_used_at: str = None,
        aliases: List[Dict[str, str]] = None,
        properties: Dict[str, str] = None,
        public: bool = None,
        auto_update: bool = None,
        cached: bool = None,
        update_source: Dict[str, Any] = None,
        type: str = None,
        profiles: List[str] = None,
        project: str = None,
        **kwargs,
    ):
        """
        Initialize a new Image model.

        Args:
            client: The Incus client instance.
            fingerprint: Fingerprint of the image.
            filename: Filename of the image.
            size: Size of the image in bytes.
            architecture: Architecture of the image.
            created_at: When the image was created.
            expires_at: When the image expires.
            uploaded_at: When the image was uploaded.
            last_used_at: When the image was last used.
            aliases: List of aliases for the image.
            properties: Properties of the image.
            public: Whether the image is public.
            auto_update: Whether the image auto-updates.
            cached: Whether the image is cached.
            update_source: Source for image updates.
            type: Type of image (container or virtual-machine).
            profiles: List of profiles to use when creating from this image.
            project: Project the image belongs to.
            **kwargs: Additional attributes to set on the model.
        """
        self.fingerprint = fingerprint
        self.filename = filename
        self.size = size
        self.architecture = architecture
        self.created_at = created_at
        self.expires_at = expires_at
        self.uploaded_at = uploaded_at
        self.last_used_at = last_used_at
        self.aliases = [ImageAlias(client=client, **alias) for alias in (aliases or [])]
        self.properties = properties or {}
        self.public = public
        self.auto_update = auto_update
        self.cached = cached
        self.update_source = update_source
        self.type = type
        self.profiles = profiles or []
        self.project = project
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the image."""
        return f"<Image: {self.fingerprint[:12]}>"

    async def delete(self, wait: bool = False) -> Dict[str, Any]:
        """
        Delete the image.

        Args:
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.images.delete(self.fingerprint, wait=wait)

    async def update(
        self, properties: Dict[str, Any], wait: bool = False
    ) -> Dict[str, Any]:
        """
        Update the image properties.

        Args:
            properties: The new properties.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.images.update(self.fingerprint, properties, wait=wait)

    async def export(self, target_path: str) -> None:
        """
        Export the image to a file.

        Args:
            target_path: Path to save the exported image.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.images.export(self.fingerprint, target_path)
