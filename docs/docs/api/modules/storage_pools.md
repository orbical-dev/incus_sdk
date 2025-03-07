# Storage Pools API

The `StoragePoolsAPI` client provides methods for managing Incus storage pools and volumes.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all storage pools
    pools = await client.storage_pools.list()
    
    # Get a storage pool by name
    pool = await client.storage_pools.get("default")
    
    # Create a new storage pool
    await client.storage_pools.create(
        name="my-pool",
        driver="dir",
        config={
            "source": "/var/lib/incus/storage-pools/my-pool"
        },
        description="My custom storage pool"
    )
    
    # List volumes in a storage pool
    volumes = await client.storage_pools.list_volumes("default")
    
    # Create a new volume
    await client.storage_pools.create_volume(
        pool_name="default",
        volume_name="my-volume",
        volume_type="custom",
        config={
            "size": "10GB"
        }
    )
    
    # Delete a storage pool
    await client.storage_pools.delete("my-pool")
```

## Class Documentation

::: incus_sdk.api.storage_pools.StoragePoolsAPI
    options:
      show_root_heading: false
      show_source: true

## Storage Pool Methods

### list

```python
async def list(recursion: int = 1) -> List[StoragePool]
```

List all storage pools.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `StoragePool` objects.

### get

```python
async def get(name: str) -> StoragePool
```

Get a storage pool by name.

**Parameters:**
- `name`: Name of the storage pool.

**Returns:**
- A `StoragePool` object.

### create

```python
async def create(
    name: str,
    driver: str,
    config: Dict[str, Any] = None,
    description: str = None,
) -> Dict[str, Any]
```

Create a new storage pool.

**Parameters:**
- `name`: Name of the storage pool.
- `driver`: Storage driver (e.g., "dir", "zfs", "btrfs", "lvm").
- `config`: Storage pool configuration as a dictionary (optional).
- `description`: Description of the storage pool (optional).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Create a directory-backed storage pool
await client.storage_pools.create(
    name="my-dir-pool",
    driver="dir",
    config={
        "source": "/var/lib/incus/storage-pools/my-dir-pool"
    },
    description="Directory-backed storage pool"
)

# Create a ZFS storage pool
await client.storage_pools.create(
    name="my-zfs-pool",
    driver="zfs",
    config={
        "source": "my-zfs-pool/incus"
    },
    description="ZFS storage pool"
)
```

### update

```python
async def update(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update a storage pool.

**Parameters:**
- `name`: Name of the storage pool.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method performs a partial update of the storage pool configuration, only modifying the specified fields.

### replace

```python
async def replace(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Replace a storage pool configuration.

**Parameters:**
- `name`: Name of the storage pool.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method replaces the entire storage pool configuration with the provided configuration.

### delete

```python
async def delete(
    name: str
) -> Dict[str, Any]
```

Delete a storage pool.

**Parameters:**
- `name`: Name of the storage pool.

**Returns:**
- The operation response as a dictionary.

## Storage Volume Methods

### list_volumes

```python
async def list_volumes(
    pool_name: str, 
    volume_type: str = None, 
    recursion: int = 1
) -> List[StorageVolume]
```

List volumes in a storage pool.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_type`: Type of volumes to list (optional). If not specified, all volume types are listed.
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `StorageVolume` objects.

**Example:**

```python
# List all volumes
all_volumes = await client.storage_pools.list_volumes("default")

# List only container volumes
container_volumes = await client.storage_pools.list_volumes("default", "container")

# List only custom volumes
custom_volumes = await client.storage_pools.list_volumes("default", "custom")
```

### get_volume

```python
async def get_volume(
    pool_name: str, 
    volume_name: str, 
    volume_type: str
) -> StorageVolume
```

Get a storage volume by name.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_name`: Name of the volume.
- `volume_type`: Type of volume (e.g., "container", "virtual-machine", "image", "custom").

**Returns:**
- A `StorageVolume` object.

### create_volume

```python
async def create_volume(
    pool_name: str,
    volume_name: str,
    volume_type: str,
    config: Dict[str, Any] = None,
) -> Dict[str, Any]
```

Create a new storage volume.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_name`: Name of the volume.
- `volume_type`: Type of volume (e.g., "container", "virtual-machine", "image", "custom").
- `config`: Volume configuration as a dictionary (optional).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Create a custom volume
await client.storage_pools.create_volume(
    pool_name="default",
    volume_name="my-volume",
    volume_type="custom",
    config={
        "size": "10GB",
        "block.filesystem": "ext4"
    }
)
```

### update_volume

```python
async def update_volume(
    pool_name: str, 
    volume_name: str, 
    volume_type: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update a storage volume.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_name`: Name of the volume.
- `volume_type`: Type of volume.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method performs a partial update of the volume configuration, only modifying the specified fields.

### replace_volume

```python
async def replace_volume(
    pool_name: str, 
    volume_name: str, 
    volume_type: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Replace a storage volume configuration.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_name`: Name of the volume.
- `volume_type`: Type of volume.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method replaces the entire volume configuration with the provided configuration.

### delete_volume

```python
async def delete_volume(
    pool_name: str, 
    volume_name: str, 
    volume_type: str
) -> Dict[str, Any]
```

Delete a storage volume.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_name`: Name of the volume.
- `volume_type`: Type of volume.

**Returns:**
- The operation response as a dictionary.

### rename_volume

```python
async def rename_volume(
    pool_name: str, 
    volume_name: str, 
    volume_type: str, 
    new_name: str
) -> Dict[str, Any]
```

Rename a storage volume.

**Parameters:**
- `pool_name`: Name of the storage pool.
- `volume_name`: Current name of the volume.
- `volume_type`: Type of volume.
- `new_name`: New name for the volume.

**Returns:**
- The operation response as a dictionary.
