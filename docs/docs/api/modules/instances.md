# Instances API

The `InstancesAPI` client provides methods for managing Incus instances (containers and virtual machines).

## Usage

```python
from incus_sdk import Client

async with Client() as client:
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
    
    # Start an instance
    await client.instances.start("my-instance", wait=True)
    
    # Stop an instance
    await client.instances.stop("my-instance", wait=True)
    
    # Delete an instance
    await client.instances.delete("my-instance", wait=True)
```

## Class Documentation

::: incus_sdk.api.instances.InstancesAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Instance]
```

List all instances.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `Instance` objects.

### get

```python
async def get(name: str) -> Instance
```

Get an instance by name.

**Parameters:**
- `name`: Name of the instance.

**Returns:**
- An `Instance` object.

### create

```python
async def create(
    name: str,
    source: Dict[str, Any],
    config: Dict[str, Any] = None,
    devices: Dict[str, Dict[str, Any]] = None,
    profiles: List[str] = None,
    ephemeral: bool = False,
    instance_type: str = "container",
    wait: bool = False,
) -> Union[Dict[str, Any], Instance]
```

Create a new instance.

**Parameters:**
- `name`: Name of the instance.
- `source`: Source configuration for the instance.
- `config`: Instance configuration (optional).
- `devices`: Instance devices (optional).
- `profiles`: List of profiles to apply (optional).
- `ephemeral`: Whether the instance is ephemeral (default: False).
- `instance_type`: Type of instance ("container" or "virtual-machine") (default: "container").
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- If `wait` is True, returns the created `Instance` object.
- If `wait` is False, returns the operation response as a dictionary.

**Example:**

```python
# Create a container from an image
container = await client.instances.create(
    name="my-container",
    source={
        "type": "image",
        "alias": "ubuntu/22.04"
    },
    config={
        "limits.cpu": "2",
        "limits.memory": "2GB"
    },
    devices={
        "root": {
            "path": "/",
            "pool": "default",
            "type": "disk"
        }
    },
    profiles=["default"],
    wait=True
)

# Create a virtual machine
vm = await client.instances.create(
    name="my-vm",
    source={
        "type": "image",
        "alias": "ubuntu/22.04"
    },
    instance_type="virtual-machine",
    wait=True
)
```

### update

```python
async def update(
    name: str, 
    config: Dict[str, Any], 
    wait: bool = False
) -> Dict[str, Any]
```

Update an instance.

**Parameters:**
- `name`: Name of the instance.
- `config`: New configuration.
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### delete

```python
async def delete(
    name: str, 
    wait: bool = False
) -> Dict[str, Any]
```

Delete an instance.

**Parameters:**
- `name`: Name of the instance.
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### start

```python
async def start(
    name: str, 
    stateful: bool = False, 
    wait: bool = False
) -> Dict[str, Any]
```

Start an instance.

**Parameters:**
- `name`: Name of the instance.
- `stateful`: Whether to restore state (default: False).
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### stop

```python
async def stop(
    name: str, 
    force: bool = False, 
    stateful: bool = False, 
    timeout: int = 30, 
    wait: bool = False
) -> Dict[str, Any]
```

Stop an instance.

**Parameters:**
- `name`: Name of the instance.
- `force`: Whether to force the stop (default: False).
- `stateful`: Whether to preserve the instance state (default: False).
- `timeout`: Timeout in seconds (default: 30).
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### restart

```python
async def restart(
    name: str, 
    force: bool = False, 
    timeout: int = 30, 
    wait: bool = False
) -> Dict[str, Any]
```

Restart an instance.

**Parameters:**
- `name`: Name of the instance.
- `force`: Whether to force the restart (default: False).
- `timeout`: Timeout in seconds (default: 30).
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### freeze

```python
async def freeze(
    name: str, 
    wait: bool = False
) -> Dict[str, Any]
```

Freeze an instance.

**Parameters:**
- `name`: Name of the instance.
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### unfreeze

```python
async def unfreeze(
    name: str, 
    wait: bool = False
) -> Dict[str, Any]
```

Unfreeze an instance.

**Parameters:**
- `name`: Name of the instance.
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### execute

```python
async def execute(
    name: str,
    command: List[str],
    environment: Dict[str, str] = None,
    wait_for_websocket: bool = False,
    record_output: bool = False,
    interactive: bool = False,
    width: int = None,
    height: int = None,
    user: int = None,
    group: int = None,
    cwd: str = None,
    wait: bool = False,
) -> Dict[str, Any]
```

Execute a command in an instance.

**Parameters:**
- `name`: Name of the instance.
- `command`: Command to execute as a list of strings.
- `environment`: Environment variables (optional).
- `wait_for_websocket`: Whether to wait for a websocket connection (default: False).
- `record_output`: Whether to record the output (default: False).
- `interactive`: Whether the command is interactive (default: False).
- `width`: Terminal width (optional).
- `height`: Terminal height (optional).
- `user`: User ID to run the command as (optional).
- `group`: Group ID to run the command as (optional).
- `cwd`: Working directory (optional).
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Execute a command and get the result
result = await client.instances.execute(
    name="my-container",
    command=["echo", "Hello, World!"],
    record_output=True,
    wait=True
)
print(result["metadata"]["output"]["stdout"])  # Prints: Hello, World!
```

### get_state

```python
async def get_state(name: str) -> Dict[str, Any]
```

Get the state of an instance.

**Parameters:**
- `name`: Name of the instance.

**Returns:**
- The instance state as a dictionary.

### get_logs

```python
async def get_logs(name: str) -> Dict[str, Any]
```

Get the logs of an instance.

**Parameters:**
- `name`: Name of the instance.

**Returns:**
- The instance logs as a dictionary.

### get_files

```python
async def get_files(
    name: str, 
    path: str
) -> bytes
```

Get files from an instance.

**Parameters:**
- `name`: Name of the instance.
- `path`: Path to the file or directory.

**Returns:**
- The file contents as bytes.

### put_files

```python
async def put_files(
    name: str, 
    path: str, 
    content: bytes
) -> Dict[str, Any]
```

Put files into an instance.

**Parameters:**
- `name`: Name of the instance.
- `path`: Path to the file or directory.
- `content`: File contents as bytes.

**Returns:**
- The operation response as a dictionary.
