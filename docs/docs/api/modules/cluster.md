# Cluster API

The `ClusterAPI` client provides methods for managing Incus clusters.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # Get cluster information
    cluster = await client.cluster.get()
    
    # List all cluster members
    members = await client.cluster.list_members()
    
    # Get a cluster member by name
    member = await client.cluster.get_member("node1")
    
    # Add a new member to the cluster
    await client.cluster.add_member(
        name="node2",
        url="10.0.0.2:8443",
        config={
            "enabled": True
        }
    )
    
    # Update a cluster member
    await client.cluster.update_member(
        "node2",
        {
            "config": {
                "enabled": False
            }
        }
    )
    
    # Delete a cluster member
    await client.cluster.delete_member("node2")
```

## Class Documentation

::: incus_sdk.api.cluster.ClusterAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### get

```python
async def get() -> Cluster
```

Get cluster information.

**Returns:**
- A `Cluster` object.

### update

```python
async def update(
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update cluster configuration.

**Parameters:**
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

### list_members

```python
async def list_members(
    recursion: int = 1
) -> List[ClusterMember]
```

List all cluster members.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `ClusterMember` objects.

### get_member

```python
async def get_member(
    name: str
) -> ClusterMember
```

Get a cluster member by name.

**Parameters:**
- `name`: Name of the cluster member.

**Returns:**
- A `ClusterMember` object.

### add_member

```python
async def add_member(
    name: str, 
    url: str, 
    config: Dict[str, Any] = None
) -> Dict[str, Any]
```

Add a new member to the cluster.

**Parameters:**
- `name`: Name of the cluster member.
- `url`: URL of the cluster member.
- `config`: Member configuration as a dictionary (optional).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Add a new member to the cluster
await client.cluster.add_member(
    name="node2",
    url="10.0.0.2:8443",
    config={
        "enabled": True,
        "role": "worker"
    }
)
```

### update_member

```python
async def update_member(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update a cluster member.

**Parameters:**
- `name`: Name of the cluster member.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

### delete_member

```python
async def delete_member(
    name: str
) -> Dict[str, Any]
```

Delete a cluster member.

**Parameters:**
- `name`: Name of the cluster member.

**Returns:**
- The operation response as a dictionary.

### rename_member

```python
async def rename_member(
    name: str, 
    new_name: str
) -> Dict[str, Any]
```

Rename a cluster member.

**Parameters:**
- `name`: Current name of the cluster member.
- `new_name`: New name for the cluster member.

**Returns:**
- The operation response as a dictionary.
