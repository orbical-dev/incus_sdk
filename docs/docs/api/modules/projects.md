# Projects API

The `ProjectsAPI` client provides methods for managing Incus projects.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all projects
    projects = await client.projects.list()
    
    # Get a project by name
    project = await client.projects.get("default")
    
    # Create a new project
    await client.projects.create(
        name="my-project",
        config={
            "features.images": "true",
            "features.profiles": "true"
        },
        description="My custom project"
    )
    
    # Update a project
    await client.projects.update(
        "my-project",
        {
            "config": {
                "features.networks": "true"
            }
        }
    )
    
    # Delete a project
    await client.projects.delete("my-project")
```

## Class Documentation

::: incus_sdk.api.projects.ProjectsAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Project]
```

List all projects.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `Project` objects.

### get

```python
async def get(name: str) -> Project
```

Get a project by name.

**Parameters:**
- `name`: Name of the project.

**Returns:**
- A `Project` object.

### create

```python
async def create(
    name: str, 
    config: Dict[str, Any] = None, 
    description: str = None
) -> Dict[str, Any]
```

Create a new project.

**Parameters:**
- `name`: Name of the project.
- `config`: Project configuration as a dictionary (optional).
- `description`: Description of the project (optional).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Create a project with specific features enabled
await client.projects.create(
    name="production",
    config={
        "features.images": "true",
        "features.profiles": "true",
        "features.storage.volumes": "true",
        "features.networks": "true",
        "restricted": "true"
    },
    description="Production environment"
)
```

### update

```python
async def update(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Update a project.

**Parameters:**
- `name`: Name of the project.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method performs a partial update of the project configuration, only modifying the specified fields.

### replace

```python
async def replace(
    name: str, 
    config: Dict[str, Any]
) -> Dict[str, Any]
```

Replace a project configuration.

**Parameters:**
- `name`: Name of the project.
- `config`: New configuration as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Note:** This method replaces the entire project configuration with the provided configuration.

### delete

```python
async def delete(
    name: str
) -> Dict[str, Any]
```

Delete a project.

**Parameters:**
- `name`: Name of the project.

**Returns:**
- The operation response as a dictionary.

### rename

```python
async def rename(
    name: str, 
    new_name: str
) -> Dict[str, Any]
```

Rename a project.

**Parameters:**
- `name`: Current name of the project.
- `new_name`: New name for the project.

**Returns:**
- The operation response as a dictionary.

### state

```python
async def state(
    name: str
) -> Dict[str, Any]
```

Get the state of a project.

**Parameters:**
- `name`: Name of the project.

**Returns:**
- The project state as a dictionary.

**Example:**

```python
# Get the state of a project
state = await client.projects.state("default")
print(f"Resources: {state.get('resources')}")
```
