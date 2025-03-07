"""
Main client for Incus API.
"""

from typing import Dict, Any, Optional, Tuple

from incus_sdk.api.client import APIClient
from incus_sdk.api.instances import InstancesAPI
from incus_sdk.api.images import ImagesAPI
from incus_sdk.api.certificates import CertificatesAPI
from incus_sdk.api.networks import NetworksAPI
from incus_sdk.api.profiles import ProfilesAPI
from incus_sdk.api.storage_pools import StoragePoolsAPI
from incus_sdk.api.cluster import ClusterAPI
from incus_sdk.api.operations import OperationsAPI
from incus_sdk.api.projects import ProjectsAPI


class Client:
    """Main client for Incus API."""

    def __init__(
        self,
        endpoint: str = None,
        cert: Optional[Tuple[str, str]] = None,
        verify: bool = True,
        project: str = None,
        timeout: int = 30,
    ):
        """
        Initialize a new Incus client.

        Args:
            endpoint: The Incus API endpoint URL.
            cert: Client certificate and key as a tuple (cert_path, key_path).
            verify: Whether to verify SSL certificates.
            project: The project to use.
            timeout: Request timeout in seconds.
        """
        self.api = APIClient(
            endpoint=endpoint,
            cert=cert,
            verify=verify,
            project=project,
            timeout=timeout,
        )

        # Initialize API clients
        self.instances = InstancesAPI(self.api)
        self.images = ImagesAPI(self.api)
        self.certificates = CertificatesAPI(self.api)
        self.networks = NetworksAPI(self.api)
        self.profiles = ProfilesAPI(self.api)
        self.storage_pools = StoragePoolsAPI(self.api)
        self.cluster = ClusterAPI(self.api)
        self.operations = OperationsAPI(self.api)
        self.projects = ProjectsAPI(self.api)

    async def __aenter__(self):
        """Enter the async context manager."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context manager."""
        await self.disconnect()

    async def connect(self):
        """Connect to the Incus API."""
        await self.api.connect()

    async def disconnect(self):
        """Disconnect from the Incus API."""
        await self.api.disconnect()

    async def get_server_info(self) -> Dict[str, Any]:
        """
        Get information about the server.

        Returns:
            Dict[str, Any]: Server information.
        """
        return await self.api.get("/1.0")

    async def get_resources(self) -> Dict[str, Any]:
        """
        Get server resources.

        Returns:
            Dict[str, Any]: Server resources.
        """
        return await self.api.get("/1.0/resources")

    async def wait_for_operation(
        self, operation_id: str, timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Wait for an operation to complete.

        Args:
            operation_id: The operation ID.
            timeout: Timeout in seconds.

        Returns:
            Dict[str, Any]: The operation result.
        """
        return await self.operations.wait(operation_id, timeout)
