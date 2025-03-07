# Error Handling

The Incus Python SDK provides a comprehensive error handling system with specific exception types for different error scenarios.

## Exception Hierarchy

- `IncusError` - Base exception for all Incus errors
- `IncusAPIError` - Exception for API request failures
- `IncusConnectionError` - Exception for connection failures
- `IncusOperationError` - Exception for operation failures
- `IncusNotFoundError` - Exception for resource not found errors
- `IncusAuthenticationError` - Exception for authentication failures
- `IncusPermissionError` - Exception for permission denied errors

## Using Exception Handling

Here's an example of how to use exception handling with the SDK:

```python
from incus_sdk import Client
from incus_sdk.exceptions import (
    IncusError,
    IncusAPIError,
    IncusConnectionError,
    IncusNotFoundError,
    IncusAuthenticationError,
    IncusPermissionError
)

async def main():
    try:
        async with Client() as client:
            try:
                # Try to get a non-existent instance
                instance = await client.instances.get("non-existent-instance")
            except IncusNotFoundError as e:
                print(f"Instance not found error: {e}")
                print(f"Response: {e.response}")
            
            try:
                # Try to create an instance with invalid parameters
                response = await client.instances.create(
                    name="test-instance",
                    source={
                        "type": "invalid-type",  # Invalid source type
                        "alias": "ubuntu/22.04"
                    },
                    wait=True
                )
            except IncusAPIError as e:
                print(f"API error: {e}")
                print(f"Status code: {e.status_code}")
                print(f"Response: {e.response}")
    
    except IncusConnectionError as e:
        print(f"Connection error: {e}")
        if hasattr(e, 'cause') and e.cause:
            print(f"Caused by: {e.cause}")
    except IncusAuthenticationError as e:
        print(f"Authentication error: {e}")
    except IncusPermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Exception Details

### IncusError

Base exception for all Incus errors.

```python
class IncusError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)
```

### IncusAPIError

Exception raised when an API request fails.

```python
class IncusAPIError(IncusError):
    def __init__(self, message: str, status_code: int, response: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code, response)
```

### IncusConnectionError

Exception raised when a connection to the Incus API fails.

```python
class IncusConnectionError(IncusError):
    def __init__(self, message: str, cause: Optional[Exception] = None):
        self.cause = cause
        super().__init__(message)
```

### IncusOperationError

Exception raised when an operation fails.

```python
class IncusOperationError(IncusError):
    def __init__(self, message: str, operation_id: str, response: Optional[Dict[str, Any]] = None):
        self.operation_id = operation_id
        super().__init__(message, response=response)
```

### IncusNotFoundError

Exception raised when a resource is not found.

```python
class IncusNotFoundError(IncusAPIError):
    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, response)
```

### IncusAuthenticationError

Exception raised when authentication fails.

```python
class IncusAuthenticationError(IncusAPIError):
    def __init__(self, message: str, status_code: int = 401, response: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code, response)
```

### IncusPermissionError

Exception raised when permission is denied.

```python
class IncusPermissionError(IncusAPIError):
    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None):
        super().__init__(message, 403, response)
```
