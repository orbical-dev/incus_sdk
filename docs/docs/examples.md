# Examples

This section provides examples of how to use the Incus Python SDK for various tasks.

## Basic Usage

```python
import asyncio
import os
import sys

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client


async def main():
    """Main function."""
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
        
        # List all images
        images = await client.images.list()
        print(f"Found {len(images)} images:")
        for image in images:
            aliases = ", ".join([alias.get("name", "") for alias in image.aliases]) if hasattr(image, "aliases") else "No aliases"
            print(f"  {image.fingerprint[:12]}: {aliases}")
        
        # List all networks
        networks = await client.networks.list()
        print(f"Found {len(networks)} networks:")
        for network in networks:
            print(f"  {network.name}: {network.type}")
        
        # List all profiles
        profiles = await client.profiles.list()
        print(f"Found {len(profiles)} profiles:")
        for profile in profiles:
            print(f"  {profile.name}")
        
        # List all storage pools
        pools = await client.storage_pools.list()
        print(f"Found {len(pools)} storage pools:")
        for pool in pools:
            print(f"  {pool.name} ({pool.driver})")


if __name__ == "__main__":
    asyncio.run(main())
```

## Instance Management

```python
import asyncio
import os
import sys
import time

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client
from incus_sdk.exceptions import IncusNotFoundError


async def main():
    """Main function."""
    # Connect to the Incus API
    async with Client() as client:
        # Create a new instance
        instance_name = f"test-instance-{int(time.time())}"
        print(f"Creating instance: {instance_name}")
        
        response = await client.instances.create(
            name=instance_name,
            source={
                "type": "image",
                "alias": "ubuntu/22.04"
            },
            instance_type="container",
            wait=True
        )
        
        print(f"Instance created: {instance_name}")
        
        # Get the instance
        instance = await client.instances.get(instance_name)
        print(f"Instance state: {instance.status}")
        
        # Start the instance
        print(f"Starting instance: {instance_name}")
        await instance.start(wait=True)
        
        # Update the instance
        print(f"Updating instance: {instance_name}")
        await instance.update(
            description="Test instance created by Incus Python SDK",
            config={
                "limits.cpu": "1",
                "limits.memory": "512MB"
            }
        )
        
        # Execute a command in the instance
        print(f"Executing command in instance: {instance_name}")
        result = await instance.execute(
            command=["echo", "Hello from Incus Python SDK!"],
            wait_for_websocket=False,
            record_output=True,
            wait=True
        )
        
        print(f"Command output: {result.get('metadata', {}).get('output', {}).get('stdout', '')}")
        
        # Stop the instance
        print(f"Stopping instance: {instance_name}")
        await instance.stop(wait=True)
        
        # Delete the instance
        print(f"Deleting instance: {instance_name}")
        await instance.delete(wait=True)
        
        print(f"Instance deleted: {instance_name}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Image Management

```python
import asyncio
import os
import sys
import time

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client


async def main():
    """Main function."""
    # Connect to the Incus API
    async with Client() as client:
        # List all images
        images = await client.images.list()
        print(f"Found {len(images)} images:")
        for image in images:
            aliases = ", ".join([alias.get("name", "") for alias in image.aliases]) if hasattr(image, "aliases") else "No aliases"
            print(f"  {image.fingerprint[:12]}: {aliases}")
        
        # Create a new image from a URL
        image_alias = f"test-image-{int(time.time())}"
        print(f"Creating image: {image_alias}")
        
        response = await client.images.create_from_url(
            url="https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-amd64-lxd.tar.xz",
            alias=image_alias,
            wait=True
        )
        
        print(f"Image created: {image_alias}")
        
        # Get the image
        image = await client.images.get_by_alias(image_alias)
        print(f"Image fingerprint: {image.fingerprint}")
        
        # Update the image
        print(f"Updating image: {image_alias}")
        await image.update(
            properties={
                "description": "Test image created by Incus Python SDK"
            }
        )
        
        # Delete the image
        print(f"Deleting image: {image_alias}")
        await image.delete()
        
        print(f"Image deleted: {image_alias}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

```python
import asyncio
import os
import sys
import time

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client
from incus_sdk.exceptions import IncusNotFoundError


async def create_network_and_profile(client):
    """Create a network and profile."""
    # Create a network
    network_name = f"test-network-{int(time.time())}"
    print(f"Creating network: {network_name}")
    
    await client.networks.create(
        name=network_name,
        description="Test network created by Incus Python SDK",
        config={
            "ipv4.address": "10.0.0.1/24",
            "ipv4.nat": "true",
            "ipv6.address": "none"
        }
    )
    
    # Create a profile that uses the network
    profile_name = f"test-profile-{int(time.time())}"
    print(f"Creating profile: {profile_name}")
    
    await client.profiles.create(
        name=profile_name,
        description="Test profile created by Incus Python SDK",
        config={
            "limits.cpu": "1",
            "limits.memory": "512MB"
        },
        devices={
            "eth0": {
                "name": "eth0",
                "network": network_name,
                "type": "nic"
            },
            "root": {
                "path": "/",
                "pool": "default",
                "type": "disk"
            }
        }
    )
    
    return network_name, profile_name


async def create_instance_with_profile(client, profile_name):
    """Create an instance with the specified profile."""
    # Create an instance using the profile
    instance_name = f"test-instance-{int(time.time())}"
    print(f"Creating instance: {instance_name}")
    
    response = await client.instances.create(
        name=instance_name,
        source={
            "type": "image",
            "alias": "ubuntu/22.04"
        },
        profiles=[profile_name],
        instance_type="container",
        wait=True
    )
    
    # Start the instance
    print(f"Starting instance: {instance_name}")
    instance = await client.instances.get(instance_name)
    await instance.start(wait=True)
    
    return instance_name


async def cleanup(client, instance_name, profile_name, network_name):
    """Clean up resources."""
    # Stop and delete the instance
    try:
        print(f"Stopping instance: {instance_name}")
        instance = await client.instances.get(instance_name)
        await instance.stop(wait=True)
        
        print(f"Deleting instance: {instance_name}")
        await instance.delete(wait=True)
    except IncusNotFoundError:
        print(f"Instance {instance_name} not found, skipping deletion")
    
    # Delete the profile
    try:
        print(f"Deleting profile: {profile_name}")
        await client.profiles.delete(profile_name)
    except IncusNotFoundError:
        print(f"Profile {profile_name} not found, skipping deletion")
    
    # Delete the network
    try:
        print(f"Deleting network: {network_name}")
        await client.networks.delete(network_name)
    except IncusNotFoundError:
        print(f"Network {network_name} not found, skipping deletion")


async def main():
    """Main function."""
    # Connect to the Incus API
    async with Client() as client:
        try:
            # Create network and profile
            network_name, profile_name = await create_network_and_profile(client)
            
            # Create instance with profile
            instance_name = await create_instance_with_profile(client, profile_name)
            
            # Wait for a moment to see the instance running
            print(f"Instance {instance_name} is running. Waiting for 5 seconds...")
            await asyncio.sleep(5)
            
            # Get instance information
            instance = await client.instances.get(instance_name)
            print(f"Instance state: {instance.status}")
            print(f"Instance addresses: {instance.state.network if hasattr(instance, 'state') and hasattr(instance.state, 'network') else 'N/A'}")
            
            # Clean up
            await cleanup(client, instance_name, profile_name, network_name)
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling

```python
import asyncio
import os
import sys
import time

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client
from incus_sdk.exceptions import (
    IncusError,
    IncusAPIError,
    IncusConnectionError,
    IncusNotFoundError,
    IncusAuthenticationError,
    IncusPermissionError,
    IncusOperationError
)


async def demonstrate_not_found_error(client):
    """Demonstrate a not found error."""
    print("\n=== Demonstrating IncusNotFoundError ===")
    try:
        # Try to get a non-existent instance
        instance = await client.instances.get("non-existent-instance")
        print(f"Instance: {instance.name}")
    except IncusNotFoundError as e:
        print(f"IncusNotFoundError: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Response: {e.response}")


async def demonstrate_api_error(client):
    """Demonstrate an API error."""
    print("\n=== Demonstrating IncusAPIError ===")
    try:
        # Try to create an instance with invalid parameters
        await client.instances.create(
            name="test-instance",
            source={
                "type": "invalid-type",  # Invalid source type
                "alias": "ubuntu/22.04"
            },
            wait=True
        )
    except IncusAPIError as e:
        print(f"IncusAPIError: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Response: {e.response}")


async def demonstrate_operation_error(client):
    """Demonstrate an operation error."""
    print("\n=== Demonstrating IncusOperationError ===")
    try:
        # Try to start a non-existent instance
        instance_name = f"test-instance-{int(time.time())}"
        
        # Create a new instance
        await client.instances.create(
            name=instance_name,
            source={
                "type": "image",
                "alias": "ubuntu/22.04"
            },
            wait=True
        )
        
        # Get the instance
        instance = await client.instances.get(instance_name)
        
        # Try to start the instance twice
        await instance.start(wait=True)
        await instance.start(wait=True)  # This should fail
    except IncusOperationError as e:
        print(f"IncusOperationError: {e}")
        print(f"Operation ID: {e.operation_id}")
        print(f"Response: {e.response}")
    finally:
        # Clean up
        try:
            instance = await client.instances.get(instance_name)
            await instance.delete(wait=True)
        except Exception:
            pass


async def main():
    """Main function."""
    try:
        # Connect to the Incus API
        async with Client() as client:
            # Demonstrate different error types
            await demonstrate_not_found_error(client)
            await demonstrate_api_error(client)
            await demonstrate_operation_error(client)
    except IncusConnectionError as e:
        print(f"IncusConnectionError: {e}")
        if hasattr(e, 'cause') and e.cause:
            print(f"Caused by: {e.cause}")
    except IncusAuthenticationError as e:
        print(f"IncusAuthenticationError: {e}")
    except IncusPermissionError as e:
        print(f"IncusPermissionError: {e}")
    except IncusError as e:
        print(f"IncusError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
```
