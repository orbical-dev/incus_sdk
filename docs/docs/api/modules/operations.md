# Operations API

The `OperationsAPI` client provides methods for managing Incus operations.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all operations
    operations = await client.operations.list()
    
    # Get an operation by ID
    operation = await client.operations.get("operation-uuid")
    
    # Wait for an operation to complete
    result = await client.operations.wait("operation-uuid", timeout=30)
    
    # Cancel an operation
    await client.operations.cancel("operation-uuid")
    
    # Delete an operation
    await client.operations.delete("operation-uuid")
```

## Class Documentation

::: incus_sdk.api.operations.OperationsAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Dict[str, Any]]
```

List all operations.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of operations as dictionaries.

### get

```python
async def get(operation_id: str) -> Dict[str, Any]
```

Get an operation by ID.

**Parameters:**
- `operation_id`: ID of the operation.

**Returns:**
- The operation as a dictionary.

**Example:**

```python
# Get an operation and check its status
operation = await client.operations.get("operation-uuid")
print(f"Operation status: {operation.get('status')}")
print(f"Operation type: {operation.get('class')}")
print(f"Operation created at: {operation.get('created_at')}")
```

### delete

```python
async def delete(operation_id: str) -> Dict[str, Any]
```

Delete an operation.

**Parameters:**
- `operation_id`: ID of the operation.

**Returns:**
- The operation response as a dictionary.

### wait

```python
async def wait(
    operation_id: str, 
    timeout: int = 60
) -> Dict[str, Any]
```

Wait for an operation to complete.

**Parameters:**
- `operation_id`: ID of the operation.
- `timeout`: Timeout in seconds (default: 60).

**Returns:**
- The operation result as a dictionary.

**Example:**

```python
# Create an instance and wait for the operation to complete
response = await client.instances.create(
    name="my-instance",
    source={
        "type": "image",
        "alias": "ubuntu/22.04"
    }
)

# Wait for the operation to complete
operation_id = response.get("metadata", {}).get("id")
if operation_id:
    result = await client.operations.wait(operation_id, timeout=120)
    if result.get("status") == "Success":
        print("Instance created successfully")
    else:
        print(f"Failed to create instance: {result.get('err')}")
```

### cancel

```python
async def cancel(operation_id: str) -> Dict[str, Any]
```

Cancel an operation.

**Parameters:**
- `operation_id`: ID of the operation.

**Returns:**
- The operation response as a dictionary.

**Note:** Not all operations can be canceled. Only long-running operations that support cancellation can be canceled.
