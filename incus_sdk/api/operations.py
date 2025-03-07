"""
Operations API client for Incus API.
"""

from typing import Dict, Any, List, Optional

from incus_sdk.api.client import APIClient


class OperationsAPI:
    """API client for Incus operations."""

    def __init__(self, client: APIClient):
        """
        Initialize a new OperationsAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Dict[str, Any]]:
        """
        List all operations.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Dict[str, Any]]: List of operations.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/operations", params=params)
        return response.get("metadata", [])

    async def get(self, operation_id: str) -> Dict[str, Any]:
        """
        Get an operation by ID.

        Args:
            operation_id: ID of the operation.

        Returns:
            Dict[str, Any]: The operation.
        """
        response = await self.client.get(f"/1.0/operations/{operation_id}")
        return response.get("metadata", {})

    async def delete(self, operation_id: str) -> Dict[str, Any]:
        """
        Delete an operation.

        Args:
            operation_id: ID of the operation.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.delete(f"/1.0/operations/{operation_id}")

    async def wait(self, operation_id: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Wait for an operation to complete.

        Args:
            operation_id: ID of the operation.
            timeout: Timeout in seconds.

        Returns:
            Dict[str, Any]: The operation result.
        """
        params = {"timeout": timeout}
        response = await self.client.get(
            f"/1.0/operations/{operation_id}/wait", params=params
        )
        return response.get("metadata", {})

    async def cancel(self, operation_id: str) -> Dict[str, Any]:
        """
        Cancel an operation.

        Args:
            operation_id: ID of the operation.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self.client.put(f"/1.0/operations/{operation_id}/cancel", data={})
