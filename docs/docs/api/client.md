# Client

The `Client` class is the main entry point for the Incus Python SDK. It provides access to all the API clients and methods for connecting to the Incus API.

## Usage

```python
from incus_sdk import Client

# Create a client
client = Client()

# Connect to the Incus API
await client.connect()

# Use the client
info = await client.get_server_info()
print(f"API version: {info.get('metadata', {}).get('api_version')}")

# Disconnect from the Incus API
await client.disconnect()
```

Alternatively, you can use the client as an async context manager:

```python
from incus_sdk import Client

async with Client() as client:
    info = await client.get_server_info()
    print(f"API version: {info.get('metadata', {}).get('api_version')}")
```

## Client Class

::: incus_sdk.client.Client
    options:
      show_root_heading: false
      show_source: true

## API Clients

The Incus Python SDK provides several API clients for interacting with different aspects of the Incus API. These clients are accessible as attributes of the `Client` class.

| Attribute | Type | Description |
|-----------|------|-------------|
| `instances` | `InstancesAPI` | API client for managing instances (containers and virtual machines) |
| `images` | `ImagesAPI` | API client for managing images |
| `networks` | `NetworksAPI` | API client for managing networks |
| `profiles` | `ProfilesAPI` | API client for managing profiles |
| `storage_pools` | `StoragePoolsAPI` | API client for managing storage pools and volumes |
| `certificates` | `CertificatesAPI` | API client for managing certificates |
| `cluster` | `ClusterAPI` | API client for managing clusters |
| `operations` | `OperationsAPI` | API client for managing operations |
| `projects` | `ProjectsAPI` | API client for managing projects |

## Client Methods

### connect

```python
async def connect()
```

Connect to the Incus API. This method is called automatically when using the client as an async context manager.

### disconnect

```python
async def disconnect()
```

Disconnect from the Incus API. This method is called automatically when using the client as an async context manager.

### get_server_info

```python
async def get_server_info() -> Dict[str, Any]
```

Get information about the Incus server.

**Returns:**
- A dictionary containing server information.

### get_resources

```python
async def get_resources() -> Dict[str, Any]
```

Get information about the resources available on the Incus server.

**Returns:**
- A dictionary containing resource information.

### wait_for_operation

```python
async def wait_for_operation(operation_id: str, timeout: int = 60) -> Dict[str, Any]
```

Wait for an operation to complete.

**Parameters:**
- `operation_id`: The ID of the operation to wait for.
- `timeout`: The maximum time to wait in seconds (default: 60).

**Returns:**
- A dictionary containing the operation result.

**Raises:**
- `IncusOperationTimeout`: If the operation does not complete within the timeout.
- `IncusOperationFailed`: If the operation fails.
