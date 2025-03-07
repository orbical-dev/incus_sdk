# Exceptions

The Incus Python SDK provides a set of exception classes for handling errors that may occur when interacting with the Incus API.

## Usage

```python
from incus_sdk import Client
from incus_sdk.exceptions import IncusNotFoundError, IncusAPIError

async def main():
    try:
        async with Client() as client:
            # Try to get a non-existent instance
            instance = await client.instances.get("non-existent-instance")
    except IncusNotFoundError as e:
        print(f"Instance not found: {e.message}")
    except IncusAPIError as e:
        print(f"API error: {e.message} (Status code: {e.status_code})")
```

## Exception Hierarchy

All exceptions in the Incus Python SDK inherit from the base `IncusError` class:

```
IncusError
├── IncusAPIError
│   ├── IncusNotFoundError
│   ├── IncusAuthenticationError
│   └── IncusPermissionError
├── IncusConnectionError
└── IncusOperationError
```

## Class Documentation

::: incus_sdk.exceptions.IncusError
    options:
      show_root_heading: true
      show_source: true

::: incus_sdk.exceptions.IncusAPIError
    options:
      show_root_heading: true
      show_source: true

::: incus_sdk.exceptions.IncusConnectionError
    options:
      show_root_heading: true
      show_source: true

::: incus_sdk.exceptions.IncusOperationError
    options:
      show_root_heading: true
      show_source: true

::: incus_sdk.exceptions.IncusNotFoundError
    options:
      show_root_heading: true
      show_source: true

::: incus_sdk.exceptions.IncusAuthenticationError
    options:
      show_root_heading: true
      show_source: true

::: incus_sdk.exceptions.IncusPermissionError
    options:
      show_root_heading: true
      show_source: true

## Exception Handling

When using the Incus Python SDK, it's important to handle exceptions properly to provide a good user experience. Here are some common exceptions you might encounter:

### IncusNotFoundError

This exception is raised when a resource (e.g., instance, image, network) is not found.

```python
try:
    instance = await client.instances.get("non-existent-instance")
except IncusNotFoundError as e:
    print(f"Instance not found: {e.message}")
```

### IncusAuthenticationError

This exception is raised when authentication fails, such as when using invalid credentials.

```python
try:
    async with Client(cert=("invalid-cert.crt", "invalid-key.key")) as client:
        await client.connect()
except IncusAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
```

### IncusPermissionError

This exception is raised when the authenticated user does not have permission to perform an action.

```python
try:
    await client.instances.create(
        name="my-instance",
        source={"type": "image", "alias": "ubuntu/22.04"}
    )
except IncusPermissionError as e:
    print(f"Permission denied: {e.message}")
```

### IncusOperationError

This exception is raised when an operation fails.

```python
try:
    await client.instances.start("my-instance", wait=True)
except IncusOperationError as e:
    print(f"Operation failed: {e.message}")
    print(f"Operation ID: {e.operation_id}")
```

### IncusConnectionError

This exception is raised when a connection to the Incus API fails.

```python
try:
    async with Client(endpoint="https://invalid-endpoint:8443") as client:
        await client.connect()
except IncusConnectionError as e:
    print(f"Connection failed: {e.message}")
    if e.cause:
        print(f"Cause: {e.cause}")
```
