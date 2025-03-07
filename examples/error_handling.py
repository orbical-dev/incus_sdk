#!/usr/bin/env python3
"""
Error handling example for the Incus Python SDK.

This example demonstrates how to handle errors from the Incus API.
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client
from incus_sdk.exceptions import (
    IncusAPIError,
    IncusConnectionError,
    IncusNotFoundError,
    IncusAuthenticationError,
    IncusPermissionError
)


async def main():
    """Main function."""
    # Connect to the Incus API
    try:
        async with Client() as client:
            # Try to get a non-existent instance
            try:
                instance = await client.instances.get("non-existent-instance")
                print(f"Instance found: {instance.name}")
            except IncusNotFoundError as e:
                print(f"Instance not found error: {e}")
                print(f"Response: {e.response}")
            
            # Try to create an instance with invalid parameters
            try:
                response = await client.instances.create(
                    name="test-instance",
                    source={
                        "type": "invalid-type",  # Invalid source type
                        "alias": "ubuntu/22.04"
                    },
                    wait=True
                )
                print(f"Instance created: {response}")
            except IncusAPIError as e:
                print(f"API error: {e}")
                print(f"Status code: {e.status_code}")
                print(f"Response: {e.response}")
            
            # Try to get a list of instances
            try:
                instances = await client.instances.list()
                print(f"Found {len(instances)} instances:")
                for instance in instances:
                    print(f"  {instance.name} ({instance.type}): {instance.status}")
            except Exception as e:
                print(f"Error listing instances: {e}")
    
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


if __name__ == "__main__":
    asyncio.run(main())
