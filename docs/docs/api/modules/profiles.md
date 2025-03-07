# Profiles API

The `ProfilesAPI` client provides methods for managing Incus profiles.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all profiles
    profiles = await client.profiles.list()
    
    # Get a profile by name
    profile = await client.profiles.get("default")
    
    # Create a new profile
    await client.profiles.create(
        name="my-profile",
        config={
            "limits.cpu": "2",
            "limits.memory": "2GB"
        },
        devices={
            "eth0": {
                "name": "eth0",
                "nictype": "bridged",
                "parent": "lxdbr0",
                "type": "nic"
            }
        },
        description="My custom profile"
    )
    
    # Update a profile
    await client.profiles.update(
        name="my-profile",
        config={
            "limits.cpu": "4",
            "limits.memory": "4GB"
        }
    )
    
    # Delete a profile
    await client.profiles.delete("my-profile")
```

## Class Documentation

::: incus_sdk.api.profiles.ProfilesAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Profile]
```

List all profiles.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `Profile` objects.

### get

```python
async def get(name: str) -> Profile
```

Get a profile by name.

**Parameters:**
- `name`: Name of the profile.

**Returns:**
- A `Profile` object.

### create

```python
async def create(
    name: str,
    config: Dict[str, Any] = None,
    description: str = None,
    devices: Dict[str, Dict[str, Any]] = None,
) -> Dict[str, Any]
```

Create a new profile.

**Parameters:**
- `name`: Name of the profile.
- `config`: Profile configuration as a dictionary (optional).
- `description`: Description of the profile (optional).
- `devices`: Profile devices as a dictionary (optional).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Create a profile with resource limits and a network device
await client.profiles.create(
    name="web-server",
    config={
        "limits.cpu": "2",
        "limits.memory": "2GB",
        "security.nesting": "true"
    },
    devices={
        "eth0": {
            "name": "eth0",
            "nictype": "bridged",
            "parent": "lxdbr0",
            "type": "nic"
        },
        "root": {
            "path": "/",
            "pool": "default",
            "type": "disk"
        }
    },
    description="Profile for web servers"
)
```

### update

```python
async def update(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update a profile.

**Parameters:**
- `name`: Name of the profile.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method performs a partial update of the profile configuration, only modifying the specified fields.

### replace

```python
async def replace(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Replace a profile configuration.

**Parameters:**
- `name`: Name of the profile.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method replaces the entire profile configuration with the provided configuration.

### delete

```python
async def delete(
    name: str
) -> Dict[str, Any]
```

Delete a profile.

**Parameters:**
- `name`: Name of the profile.

**Returns:**
- The operation response as a dictionary.

### rename

```python
async def rename(
    name: str, 
    new_name: str
) -> Dict[str, Any]
```

Rename a profile.

**Parameters:**
- `name`: Current name of the profile.
- `new_name`: New name for the profile.

**Returns:**
- The operation response as a dictionary.
