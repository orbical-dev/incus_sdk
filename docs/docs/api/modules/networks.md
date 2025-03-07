# Networks API

The `NetworksAPI` client provides methods for managing Incus networks.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all networks
    networks = await client.networks.list()
    
    # Get a network by name
    network = await client.networks.get("lxdbr0")
    
    # Create a new network
    await client.networks.create(
        name="my-network",
        config={
            "ipv4.address": "10.0.0.1/24",
            "ipv4.nat": "true",
            "ipv6.address": "fd42:474b:622d:259d::1/64",
            "ipv6.nat": "true"
        },
        description="My custom network"
    )
    
    # Update a network
    await client.networks.update(
        name="my-network",
        config={
            "ipv4.dhcp": "true",
            "ipv6.dhcp": "true"
        }
    )
    
    # Delete a network
    await client.networks.delete("my-network")
```

## Class Documentation

::: incus_sdk.api.networks.NetworksAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Network]
```

List all networks.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `Network` objects.

### get

```python
async def get(name: str) -> Network
```

Get a network by name.

**Parameters:**
- `name`: Name of the network.

**Returns:**
- A `Network` object.

### create

```python
async def create(
    name: str,
    config: Dict[str, Any],
    description: str = None,
    type: str = "bridge",
) -> Dict[str, Any]
```

Create a new network.

**Parameters:**
- `name`: Name of the network.
- `config`: Network configuration as a dictionary.
- `description`: Description of the network (optional).
- `type`: Type of network (default: "bridge").

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Create a bridge network
await client.networks.create(
    name="my-network",
    config={
        "ipv4.address": "10.0.0.1/24",
        "ipv4.nat": "true",
        "ipv4.dhcp": "true",
        "ipv6.address": "fd42:474b:622d:259d::1/64",
        "ipv6.nat": "true",
        "ipv6.dhcp": "true"
    },
    description="My custom network",
    type="bridge"
)
```

### update

```python
async def update(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update a network.

**Parameters:**
- `name`: Name of the network.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method performs a partial update of the network configuration, only modifying the specified fields.

### replace

```python
async def replace(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Replace a network configuration.

**Parameters:**
- `name`: Name of the network.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method replaces the entire network configuration with the provided configuration.

### delete

```python
async def delete(
    name: str
) -> Dict[str, Any]
```

Delete a network.

**Parameters:**
- `name`: Name of the network.

**Returns:**
- The operation response as a dictionary.

### rename

```python
async def rename(
    name: str, 
    new_name: str
) -> Dict[str, Any]
```

Rename a network.

**Parameters:**
- `name`: Current name of the network.
- `new_name`: New name for the network.

**Returns:**
- The operation response as a dictionary.

### state

```python
async def state(
    name: str
) -> Dict[str, Any]
```

Get the state of a network.

**Parameters:**
- `name`: Name of the network.

**Returns:**
- The network state as a dictionary.

**Example:**

```python
# Get the state of a network
state = await client.networks.state("lxdbr0")
print(f"DHCP leases: {state.get('leases')}")
```
