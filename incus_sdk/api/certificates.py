"""
Certificates API client for Incus API.
"""

from typing import Dict, Any, List, Optional

from incus_sdk.api.client import APIClient
from incus_sdk.models.certificate import Certificate


class CertificatesAPI:
    """API client for Incus certificates."""

    def __init__(self, client: APIClient):
        """
        Initialize a new CertificatesAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Certificate]:
        """
        List all certificates.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Certificate]: List of certificates.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/certificates", params=params)

        certificates = []
        for cert_data in response.get("metadata", []):
            certificates.append(Certificate(client=self, **cert_data))

        return certificates

    async def get(self, fingerprint: str) -> Certificate:
        """
        Get a certificate by fingerprint.

        Args:
            fingerprint: Fingerprint of the certificate.

        Returns:
            Certificate: The certificate.
        """
        response = await self.client.get(f"/1.0/certificates/{fingerprint}")
        return Certificate(client=self, **response.get("metadata", {}))

    async def create(
        self,
        certificate: str,
        name: str = None,
        type: str = "client",
        restricted: bool = False,
        projects: List[str] = None,
        password: str = None,
    ) -> Dict[str, Any]:
        """
        Create a new certificate.

        Args:
            certificate: Certificate data.
            name: Name of the certificate.
            type: Type of certificate.
            restricted: Whether the certificate is restricted.
            projects: List of projects the certificate has access to.
            password: Password for the certificate.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {"certificate": certificate, "type": type, "restricted": restricted}

        if name:
            data["name"] = name
        if projects:
            data["projects"] = projects
        if password:
            data["password"] = password

        return await self.client.post("/1.0/certificates", data=data)

    async def delete(self, fingerprint: str) -> Dict[str, Any]:
        """
        Delete a certificate.

        Args:
            fingerprint: Fingerprint of the certificate.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/certificates/{fingerprint}")

    async def update(self, fingerprint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a certificate.

        Args:
            fingerprint: Fingerprint of the certificate.
            data: New certificate data.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.patch(f"/1.0/certificates/{fingerprint}", data=data)
