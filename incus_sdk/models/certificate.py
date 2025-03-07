"""
Certificate model for Incus resources.
"""

from typing import Dict, Any, Optional
from incus_sdk.models.base import Model


class Certificate(Model):
    """Model representing an Incus certificate."""

    def __init__(
        self,
        client=None,
        fingerprint: str = None,
        certificate: str = None,
        name: str = None,
        type: str = None,
        restricted: bool = None,
        projects: list = None,
        **kwargs,
    ):
        """
        Initialize a new Certificate model.

        Args:
            client: The Incus client instance.
            fingerprint: Fingerprint of the certificate.
            certificate: The certificate data.
            name: Name of the certificate.
            type: Type of certificate.
            restricted: Whether the certificate is restricted.
            projects: List of projects the certificate has access to.
            **kwargs: Additional attributes to set on the model.
        """
        self.fingerprint = fingerprint
        self.certificate = certificate
        self.name = name
        self.type = type
        self.restricted = restricted
        self.projects = projects or []
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the certificate."""
        return f"<Certificate: {self.name or self.fingerprint}>"

    async def delete(self) -> Dict[str, Any]:
        """
        Delete the certificate.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.certificates.delete(self.fingerprint)

    async def update(
        self,
        name: Optional[str] = None,
        type: Optional[str] = None,
        restricted: Optional[bool] = None,
        projects: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Update the certificate.

        Args:
            name: New name for the certificate.
            type: New type for the certificate.
            restricted: Whether the certificate should be restricted.
            projects: New list of projects the certificate has access to.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        data = {}
        if name is not None:
            data["name"] = name
        if type is not None:
            data["type"] = type
        if restricted is not None:
            data["restricted"] = restricted
        if projects is not None:
            data["projects"] = projects

        return await self._client.certificates.update(self.fingerprint, data)
