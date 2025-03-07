# Images API

The `ImagesAPI` client provides methods for managing Incus images.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all images
    images = await client.images.list()
    
    # Get an image by fingerprint
    image = await client.images.get("abcdef123456")
    
    # Create an image from a file
    with open("image.tar.gz", "rb") as f:
        image_data = f.read()
    
    await client.images.create(
        image_data=image_data,
        filename="image.tar.gz",
        properties={"description": "My custom image"},
        wait=True
    )
    
    # Export an image to a file
    await client.images.export("abcdef123456", "exported_image.tar.gz")
    
    # Create an alias for an image
    await client.images.create_alias(
        name="my-image",
        target="abcdef123456",
        description="My custom image"
    )
    
    # Delete an image
    await client.images.delete("abcdef123456", wait=True)
```

## Class Documentation

::: incus_sdk.api.images.ImagesAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Image]
```

List all images.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `Image` objects.

### get

```python
async def get(fingerprint: str) -> Image
```

Get an image by fingerprint.

**Parameters:**
- `fingerprint`: Fingerprint of the image.

**Returns:**
- An `Image` object.

### create

```python
async def create(
    image_data: bytes,
    filename: str = None,
    public: bool = False,
    auto_update: bool = False,
    properties: Dict[str, str] = None,
    wait: bool = False,
) -> Union[Dict[str, Any], Image]
```

Create a new image.

**Parameters:**
- `image_data`: Image data as bytes.
- `filename`: Name of the image file (optional).
- `public`: Whether the image is public (default: False).
- `auto_update`: Whether the image auto-updates (default: False).
- `properties`: Image properties as a dictionary (optional).
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- If `wait` is True, returns the created `Image` object.
- If `wait` is False, returns the operation response as a dictionary.

**Example:**

```python
# Create an image from a file
import aiofiles

async with aiofiles.open("image.tar.gz", "rb") as f:
    image_data = await f.read()

image = await client.images.create(
    image_data=image_data,
    filename="image.tar.gz",
    properties={
        "description": "My custom image",
        "os": "Ubuntu",
        "release": "22.04"
    },
    public=True,
    wait=True
)
```

### delete

```python
async def delete(
    fingerprint: str, 
    wait: bool = False
) -> Dict[str, Any]
```

Delete an image.

**Parameters:**
- `fingerprint`: Fingerprint of the image.
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### update

```python
async def update(
    fingerprint: str, 
    properties: Dict[str, Any], 
    wait: bool = False
) -> Dict[str, Any]
```

Update an image.

**Parameters:**
- `fingerprint`: Fingerprint of the image.
- `properties`: New properties as a dictionary.
- `wait`: Whether to wait for the operation to complete (default: False).

**Returns:**
- The operation response as a dictionary.

### export

```python
async def export(
    fingerprint: str, 
    target_path: str
) -> None
```

Export an image to a file.

**Parameters:**
- `fingerprint`: Fingerprint of the image.
- `target_path`: Path to save the exported image.

**Returns:**
- None

### create_alias

```python
async def create_alias(
    name: str, 
    target: str, 
    description: str = None
) -> Dict[str, Any]
```

Create an image alias.

**Parameters:**
- `name`: Name of the alias.
- `target`: Target fingerprint.
- `description`: Description of the alias (optional).

**Returns:**
- The operation response as a dictionary.

### delete_alias

```python
async def delete_alias(
    name: str
) -> Dict[str, Any]
```

Delete an image alias.

**Parameters:**
- `name`: Name of the alias.

**Returns:**
- The operation response as a dictionary.

### get_alias

```python
async def get_alias(
    name: str
) -> Dict[str, Any]
```

Get an image alias.

**Parameters:**
- `name`: Name of the alias.

**Returns:**
- The alias information as a dictionary.

### update_alias

```python
async def update_alias(
    name: str, 
    target: str, 
    description: str = None
) -> Dict[str, Any]
```

Update an image alias.

**Parameters:**
- `name`: Name of the alias.
- `target`: New target fingerprint.
- `description`: New description (optional).

**Returns:**
- The operation response as a dictionary.
