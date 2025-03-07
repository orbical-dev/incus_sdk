"""
Utility functions for the Incus Python SDK.
"""

import asyncio
import os
from typing import Dict, Any, Optional, List, Union, Callable, Awaitable


async def wait_for_operation(
    operation_id: str,
    client,
    timeout: int = 60,
    interval: float = 0.5,
    callback: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
) -> Dict[str, Any]:
    """
    Wait for an operation to complete.

    Args:
        operation_id: The operation ID.
        client: The Incus client.
        timeout: Timeout in seconds.
        interval: Polling interval in seconds.
        callback: Optional callback function to call with operation status.

    Returns:
        Dict[str, Any]: The operation result.

    Raises:
        TimeoutError: If the operation times out.
    """
    start_time = asyncio.get_event_loop().time()
    while True:
        operation = await client.operations.get(operation_id)

        # Call the callback if provided
        if callback:
            await callback(operation)

        # Check if the operation is done
        if operation.get("status") == "Success":
            return operation
        elif operation.get("status") == "Failure":
            error = operation.get("err", "Unknown error")
            raise Exception(f"Operation failed: {error}")

        # Check for timeout
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(f"Operation timed out after {timeout} seconds")

        # Wait before polling again
        await asyncio.sleep(interval)


def parse_unix_socket_path(path: str) -> str:
    """
    Parse a Unix socket path.

    Args:
        path: The socket path.

    Returns:
        str: The normalized socket path.
    """
    if path.startswith("unix://"):
        path = path[7:]

    # Expand home directory
    if path.startswith("~"):
        path = os.path.expanduser(path)

    # Make absolute path
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    return path


def format_instance_config(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Format instance configuration.

    Args:
        config: Instance configuration.

    Returns:
        Dict[str, str]: Formatted configuration.
    """
    formatted = {}
    for key, value in config.items():
        if isinstance(value, bool):
            formatted[key] = "true" if value else "false"
        elif isinstance(value, (int, float)):
            formatted[key] = str(value)
        elif value is None:
            continue
        else:
            formatted[key] = str(value)
    return formatted


def format_size(size_bytes: int) -> str:
    """
    Format size in bytes to human-readable format.

    Args:
        size_bytes: Size in bytes.

    Returns:
        str: Human-readable size.
    """
    if size_bytes == 0:
        return "0B"

    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1

    return f"{size_bytes:.2f}{size_names[i]}"
