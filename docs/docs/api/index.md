# API Reference

This section provides detailed API documentation for the Incus Python SDK.

## Client

The `Client` class is the main entry point for the Incus Python SDK. It provides access to all the API clients and methods for connecting to the Incus API.

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

### Client Class

```python
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
```

### Client Attributes

- `api` - The underlying API client.
- `instances` - API client for managing instances.
- `images` - API client for managing images.
- `certificates` - API client for managing certificates.
- `networks` - API client for managing networks.
- `profiles` - API client for managing profiles.
- `storage_pools` - API client for managing storage pools.
- `cluster` - API client for managing clusters.
- `operations` - API client for managing operations.
- `projects` - API client for managing projects.

### Client Methods

- `async connect()` - Connect to the Incus API.
- `async disconnect()` - Disconnect from the Incus API.
- `async get_server_info()` - Get information about the server.
- `async get_resources()` - Get server resources.
- `async wait_for_operation(operation_id, timeout=60)` - Wait for an operation to complete.

## API Clients

The Incus Python SDK provides several API clients for interacting with different aspects of the Incus API.

### InstancesAPI

The `InstancesAPI` client provides methods for managing Incus instances (containers and virtual machines).

```python
# List all instances
instances = await client.instances.list()

# Create a new instance
await client.instances.create(
    name="my-instance",
    source={
        "type": "image",
        "alias": "ubuntu/22.04"
    },
    wait=True
)

# Get an instance
instance = await client.instances.get("my-instance")

# Delete an instance
await client.instances.delete("my-instance")
```

### ImagesAPI

The `ImagesAPI` client provides methods for managing Incus images.

```python
# List all images
images = await client.images.list()

# Create a new image from a URL
await client.images.create_from_url(
    url="https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-amd64-lxd.tar.xz",
    alias="ubuntu/22.04",
    wait=True
)

# Get an image
image = await client.images.get("my-image")

# Delete an image
await client.images.delete("my-image")
```

### NetworksAPI

The `NetworksAPI` client provides methods for managing Incus networks.

```python
# List all networks
networks = await client.networks.list()

# Create a new network
await client.networks.create(
    name="my-network",
    description="My network",
    config={
        "ipv4.address": "10.0.0.1/24",
        "ipv4.nat": "true",
        "ipv6.address": "none"
    }
)

# Get a network
network = await client.networks.get("my-network")

# Delete a network
await client.networks.delete("my-network")
```

### ProfilesAPI

The `ProfilesAPI` client provides methods for managing Incus profiles.

```python
# List all profiles
profiles = await client.profiles.list()

# Create a new profile
await client.profiles.create(
    name="my-profile",
    description="My profile",
    config={
        "limits.cpu": "1",
        "limits.memory": "512MB"
    },
    devices={
        "eth0": {
            "name": "eth0",
            "network": "lxdbr0",
            "type": "nic"
        },
        "root": {
            "path": "/",
            "pool": "default",
            "type": "disk"
        }
    }
)

# Get a profile
profile = await client.profiles.get("my-profile")

# Delete a profile
await client.profiles.delete("my-profile")
```

### StoragePoolsAPI

The `StoragePoolsAPI` client provides methods for managing Incus storage pools and volumes.

```python
# List all storage pools
pools = await client.storage_pools.list()

# Create a new storage pool
await client.storage_pools.create(
    name="my-pool",
    description="My storage pool",
    driver="dir",
    config={
        "source": "/var/lib/incus/storage-pools/my-pool"
    }
)

# Get a storage pool
pool = await client.storage_pools.get("my-pool")

# Delete a storage pool
await client.storage_pools.delete("my-pool")
```

### CertificatesAPI

The `CertificatesAPI` client provides methods for managing Incus certificates.

```python
# List all certificates
certificates = await client.certificates.list()

# Create a new certificate
with open("client.crt", "r") as f:
    cert_data = f.read()

await client.certificates.create(
    certificate=cert_data,
    name="my-client",
    type="client",
    restricted=True
)

# Get a certificate
certificate = await client.certificates.get("abcdef123456")

# Delete a certificate
await client.certificates.delete("abcdef123456")
```

### ClusterAPI

The `ClusterAPI` client provides methods for managing Incus clusters.

```python
# Get cluster information
cluster = await client.cluster.get()

# List all cluster members
members = await client.cluster.list_members()

# Add a new member to the cluster
await client.cluster.add_member(
    name="node2",
    url="10.0.0.2:8443"
)

# Delete a cluster member
await client.cluster.delete_member("node2")
```

### OperationsAPI

The `OperationsAPI` client provides methods for managing Incus operations.

```python
# List all operations
operations = await client.operations.list()

# Get an operation by ID
operation = await client.operations.get("operation-uuid")

# Wait for an operation to complete
result = await client.operations.wait("operation-uuid", timeout=30)

# Cancel an operation
await client.operations.cancel("operation-uuid")
```

### ProjectsAPI

The `ProjectsAPI` client provides methods for managing Incus projects.

```python
# List all projects
projects = await client.projects.list()

# Create a new project
await client.projects.create(
    name="my-project",
    config={
        "features.images": "true",
        "features.profiles": "true"
    },
    description="My custom project"
)

# Get a project
project = await client.projects.get("my-project")

# Delete a project
await client.projects.delete("my-project")
```

## Exceptions

The Incus Python SDK provides a set of exception classes for handling errors that may occur when interacting with the Incus API.

```python
from incus_sdk.exceptions import IncusNotFoundError, IncusAPIError

try:
    instance = await client.instances.get("non-existent-instance")
except IncusNotFoundError as e:
    print(f"Instance not found: {e.message}")
except IncusAPIError as e:
    print(f"API error: {e.message} (Status code: {e.status_code})")
```

See the [Exceptions](exceptions.md) page for more details on the available exception classes and how to handle them.

## Models

The Incus Python SDK provides model classes for representing Incus resources. These models provide a convenient way to access resource properties and perform operations on resources.

See the [Models](models.md) page for more details on the available model classes.

## API Modules (continued)

The `ClusterAPI` client provides methods for managing Incus clusters.

```python
# Get the cluster
cluster = await client.cluster.get()

# List all cluster members
members = await client.cluster.list_members()

# Get a cluster member
member = await client.cluster.get_member("member1")

# Remove a cluster member
await client.cluster.remove_member("member1")
```

### OperationsAPI

The `OperationsAPI` client provides methods for managing Incus operations.

```python
# List all operations
operations = await client.operations.list()

# Get an operation
operation = await client.operations.get("operation-id")

# Wait for an operation to complete
result = await client.operations.wait("operation-id")

# Cancel an operation
await client.operations.cancel("operation-id")
```

### ProjectsAPI

The `ProjectsAPI` client provides methods for managing Incus projects.

```python
# List all projects
projects = await client.projects.list()

# Create a new project
await client.projects.create(
    name="my-project",
    description="My project",
    config={
        "features.images": "true",
        "features.profiles": "true"
    }
)

# Get a project
project = await client.projects.get("my-project")

# Delete a project
await client.projects.delete("my-project")
```
