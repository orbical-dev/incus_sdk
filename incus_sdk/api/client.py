"""
Base API client for Incus API.
"""

import json
import os
import ssl
import urllib.parse
from typing import Dict, Any, Optional, Tuple

import aiohttp
import certifi

from incus_sdk.exceptions import (
    IncusAPIError,
    IncusConnectionError,
    IncusNotFoundError,
    IncusAuthenticationError,
    IncusPermissionError,
)


class APIClient:
    """Base API client for Incus API."""

    def __init__(
        self,
        endpoint: str = None,
        cert: Optional[Tuple[str, str]] = None,
        verify: bool = True,
        project: str = None,
        timeout: int = 30,
    ):
        """
        Initialize a new API client.

        Args:
            endpoint: The Incus API endpoint URL.
            cert: Client certificate and key as a tuple (cert_path, key_path).
            verify: Whether to verify SSL certificates.
            project: The project to use.
            timeout: Request timeout in seconds.
        """
        self.endpoint = endpoint or os.environ.get(
            "INCUS_ENDPOINT", "unix:///var/lib/incus/unix.socket"
        )
        self.cert = cert
        self.verify = verify
        self.project = project
        self.timeout = timeout
        self._session = None

    async def __aenter__(self):
        """Enter the async context manager."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context manager."""
        await self.disconnect()

    async def connect(self):
        """Connect to the Incus API."""
        try:
            if self._session is None:
                ssl_context = None
                if self.endpoint.startswith("https://"):
                    ssl_context = ssl.create_default_context(
                        cafile=certifi.where()
                    )
                    if not self.verify:
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE
                    if self.cert:
                        ssl_context.load_cert_chain(self.cert[0], self.cert[1])

                connector = None
                if self.endpoint.startswith("unix://"):
                    socket_path = self.endpoint.replace("unix://", "")
                    connector = aiohttp.UnixConnector(path=socket_path)

                self._session = aiohttp.ClientSession(
                    connector=connector,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                )
        except Exception as e:
            raise IncusConnectionError(
                f"Failed to connect to Incus API: {str(e)}",
                cause=e
            )

    async def disconnect(self):
        """Disconnect from the Incus API."""
        if self._session:
            await self._session.close()
            self._session = None

    def _build_url(self, path: str, params: Dict[str, Any] = None) -> str:
        """
        Build a URL for the API request.

        Args:
            path: The API path.
            params: Query parameters.

        Returns:
            str: The full URL.
        """
        if self.endpoint.startswith("unix://"):
            url = f"http://localhost{path}"
        else:
            url = f"{self.endpoint}{path}"

        # Add project parameter if specified
        if self.project and params is None:
            params = {"project": self.project}
        elif self.project:
            params["project"] = self.project

        # Add query parameters
        if params:
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"

        return url

    async def request(
        self,
        method: str,
        path: str,
        params: Dict[str, Any] = None,
        data: Any = None,
        headers: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """
        Make an API request.

        Args:
            method: HTTP method.
            path: API path.
            params: Query parameters.
            data: Request data.
            headers: Request headers.

        Returns:
            Dict[str, Any]: The API response.

        Raises:
            Exception: If the request fails.
        """
        if self._session is None:
            await self.connect()

        url = self._build_url(path, params)
        headers = headers or {}

        if data is not None and not isinstance(data, (str, bytes)):
            data = json.dumps(data)
            headers["Content-Type"] = "application/json"

        try:
            async with self._session.request(
                method, url, data=data, headers=headers, ssl=None
            ) as response:
                content = await response.text()
                if content:
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError as e:
                        raise IncusAPIError(
                            f"Invalid JSON response: {str(e)}",
                            status_code=500
                        )

                if response.status >= 400:
                    error_msg = ""
                    if isinstance(content, dict) and "error" in content:
                        error_msg = content["error"]
                    elif isinstance(content, str):
                        error_msg = content

                    if response.status == 404:
                        raise IncusNotFoundError(
                            error_msg or f"Resource not found: {path}",
                            response=content
                        )
                    elif response.status == 401:
                        raise IncusAuthenticationError(
                            error_msg or "Authentication failed",
                            response=content
                        )
                    elif response.status == 403:
                        raise IncusPermissionError(
                            error_msg or "Permission denied",
                            response=content
                        )
                    else:
                        raise IncusAPIError(
                            error_msg or f"API error: {response.status}",
                            status_code=response.status,
                            response=content
                        )

                return content
        except aiohttp.ClientError as e:
            raise IncusConnectionError(f"Connection error: {str(e)}", cause=e)

    async def get(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a GET request.

        Args:
            path: API path.
            params: Query parameters.

        Returns:
            Dict[str, Any]: The API response.
        """
        return await self.request("GET", path, params=params)

    async def post(
        self, path: str, data: Any = None, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make a POST request.

        Args:
            path: API path.
            data: Request data.
            params: Query parameters.

        Returns:
            Dict[str, Any]: The API response.
        """
        return await self.request("POST", path, data=data, params=params)

    async def put(
        self, path: str, data: Any = None, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make a PUT request.

        Args:
            path: API path.
            data: Request data.
            params: Query parameters.

        Returns:
            Dict[str, Any]: The API response.
        """
        return await self.request("PUT", path, data=data, params=params)

    async def patch(
        self, path: str, data: Any = None, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make a PATCH request.

        Args:
            path: API path.
            data: Request data.
            params: Query parameters.

        Returns:
            Dict[str, Any]: The API response.
        """
        return await self.request("PATCH", path, data=data, params=params)

    async def delete(
        self, path: str, data: Any = None, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make a DELETE request.

        Args:
            path: API path.
            data: Request data.
            params: Query parameters.

        Returns:
            Dict[str, Any]: The API response.
        """
        return await self.request("DELETE", path, data=data, params=params)

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

        Raises:
            TimeoutError: If the operation times out.
            Exception: If the operation fails.
        """
        path = f"/1.0/operations/{operation_id}/wait"
        params = {"timeout": timeout}
        result = await self.get(path, params=params)

        if result.get("status") == "Failure":
            raise Exception(
                f"Operation failed: {result.get('err')}"
            )

        return result
