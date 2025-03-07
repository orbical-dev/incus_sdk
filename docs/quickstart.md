# Quick Start

This guide will help you get started with the Incus Python SDK.

## Basic Usage

Here's a simple example of how to use the SDK:

```python
import asyncio
from incus_sdk import Client

async def main():
    # Connect to the Incus API
    async with Client() as client:
        # Get server information
        info = await client.get_server_info()
        print(f"API version: {info.get('metadata', {}).get('api_version')}")
        
        # List all instances
        instances = await client.instances.list()
        print(f"Found {len(instances)} instances:")
        for instance in instances:
            print(f"  {instance.name} ({instance.type}): {instance.status}")
        
        # Create a new container
        response = await client.instances.create(
            name="my-container",
            source={
                "type": "image",
                "alias": "ubuntu/22.04"
            },
            wait=True
        )
        
        # Get the container
        container = await client.instances.get("my-container")
        
        # Start the container
        await container.start(wait=True)
        
        # Execute a command in the container
        response = await container.execute(
            command=["echo", "Hello from Incus Python SDK!"],
            wait_for_websocket=False,
            record_output=True,
            wait=True
        )
        
        # Stop the container
        await container.stop(wait=True)
        
        # Delete the container
        await container.delete(wait=True)

if __name__ == "__main__":
    asyncio.run(main())
```

## Connection Options

The SDK supports connecting to both local and remote Incus servers:

```python
# Connect to local Unix socket (default)
client = Client()

# Connect to local HTTPS endpoint
client = Client(endpoint="https://localhost:8443")

# Connect to remote HTTPS endpoint with certificate
client = Client(
    endpoint="https://example.com:8443",
    cert=("/path/to/client.crt", "/path/to/client.key"),
    verify=True
)

# Connect to remote HTTPS endpoint without certificate verification
client = Client(
    endpoint="https://example.com:8443",
    verify=False
)

# Connect to a specific project
client = Client(project="my-project")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from incus_sdk import Client
from incus_sdk.exceptions import IncusNotFoundError, IncusAPIError

async def main():
    async with Client() as client:
        try:
            # Try to get a non-existent instance
            instance = await client.instances.get("non-existent")
        except IncusNotFoundError as e:
            print(f"Instance not found: {e}")
        
        try:
            # Try to create an instance with invalid parameters
            await client.instances.create(
                name="test-instance",
                source={
                    "type": "invalid-type",
                    "alias": "ubuntu/22.04"
                }
            )
        except IncusAPIError as e:
            print(f"API error: {e}, Status code: {e.status_code}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Working with Resources

The SDK provides model classes for working with Incus resources:

```python
from incus_sdk import Client

async def main():
    async with Client() as client:
        # Get an instance
        instance = await client.instances.get("my-instance")
        
        # Access instance properties
        print(f"Name: {instance.name}")
        print(f"Type: {instance.type}")
        print(f"Status: {instance.status}")
        
        # Start the instance
        await instance.start()
        
        # Stop the instance
        await instance.stop()
        
        # Delete the instance
        await instance.delete()

if __name__ == "__main__":
    asyncio.run(main())
```
