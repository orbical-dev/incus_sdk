# Utilities

The Incus Python SDK provides a set of utility functions to help with common tasks when working with Incus.

## wait_for_operation

The `wait_for_operation` function allows you to wait for an Incus operation to complete.

```python
from incus_sdk import Client
from incus_sdk.utils import wait_for_operation

async with Client() as client:
    # Start an instance
    operation = await client.instances.start("my-instance")
    
    # Wait for the operation to complete
    result = await wait_for_operation(operation["id"], client)
    
    # You can also specify a timeout and polling interval
    result = await wait_for_operation(
        operation["id"],
        client,
        timeout=120,  # 2 minutes
        interval=1.0  # Check every second
    )
    
    # You can provide a callback function to be called with operation status
    async def status_callback(operation):
        print(f"Operation status: {operation.get('status')}")
    
    result = await wait_for_operation(
        operation["id"],
        client,
        callback=status_callback
    )
```

### Parameters

- `operation_id` (str): The operation ID.
- `client`: The Incus client.
- `timeout` (int, optional): Timeout in seconds. Default is 60.
- `interval` (float, optional): Polling interval in seconds. Default is 0.5.
- `callback` (callable, optional): Optional callback function to call with operation status.

### Returns

- `Dict[str, Any]`: The operation result.

### Raises

- `TimeoutError`: If the operation times out.
- `Exception`: If the operation fails.

## parse_unix_socket_path

The `parse_unix_socket_path` function normalizes a Unix socket path.

```python
from incus_sdk.utils import parse_unix_socket_path

# Parse a socket path
socket_path = parse_unix_socket_path("unix:///var/lib/incus/unix.socket")
# Returns: "/var/lib/incus/unix.socket"

# Expand home directory
socket_path = parse_unix_socket_path("~/incus/unix.socket")
# Returns: "/home/user/incus/unix.socket"
```

### Parameters

- `path` (str): The socket path.

### Returns

- `str`: The normalized socket path.

## format_instance_config

The `format_instance_config` function formats instance configuration values to strings.

```python
from incus_sdk.utils import format_instance_config

# Format instance configuration
config = {
    "limits.cpu": 2,
    "limits.memory": "2GB",
    "security.privileged": True,
    "environment.DEBUG": None
}

formatted_config = format_instance_config(config)
# Returns: {
#   "limits.cpu": "2",
#   "limits.memory": "2GB",
#   "security.privileged": "true"
# }
```

### Parameters

- `config` (Dict[str, Any]): Instance configuration.

### Returns

- `Dict[str, str]`: Formatted configuration.

## format_size

The `format_size` function formats a size in bytes to a human-readable format.

```python
from incus_sdk.utils import format_size

# Format size in bytes
size = format_size(1024)  # Returns: "1.00KB"
size = format_size(1048576)  # Returns: "1.00MB"
size = format_size(1073741824)  # Returns: "1.00GB"
```

### Parameters

- `size_bytes` (int): Size in bytes.

### Returns

- `str`: Human-readable size.
