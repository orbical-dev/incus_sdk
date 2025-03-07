#!/usr/bin/env python3
"""
Instance management example for the Incus Python SDK.

This example demonstrates how to create, manage, and delete instances.
"""

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
        # Define the instance name
        instance_name = f"test-container-{int(time.time())}"
        
        print(f"Creating instance: {instance_name}")
        
        # Create a new container
        response = await client.instances.create(
            name=instance_name,
            source={
                "type": "image",
                "alias": "ubuntu/22.04"
            },
            config={
                "limits.cpu": "1",
                "limits.memory": "512MB"
            },
            profiles=["default"],
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
        
        # Refresh the instance state
        instance = await client.instances.get(instance_name)
        print(f"Instance state after start: {instance.status}")
        
        # Execute a command in the instance
        print(f"Executing command in instance: {instance_name}")
        response = await instance.execute(
            command=["echo", "Hello from Incus Python SDK!"],
            wait_for_websocket=False,
            record_output=True,
            wait=True
        )
        
        # Get the command output
        if "metadata" in response and "output" in response["metadata"]:
            stdout = response["metadata"]["output"].get("stdout", "")
            stderr = response["metadata"]["output"].get("stderr", "")
            print(f"Command output (stdout): {stdout.decode('utf-8') if isinstance(stdout, bytes) else stdout}")
            print(f"Command output (stderr): {stderr.decode('utf-8') if isinstance(stderr, bytes) else stderr}")
        
        # Stop the instance
        print(f"Stopping instance: {instance_name}")
        await instance.stop(wait=True)
        
        # Refresh the instance state
        instance = await client.instances.get(instance_name)
        print(f"Instance state after stop: {instance.status}")
        
        # Delete the instance
        print(f"Deleting instance: {instance_name}")
        await instance.delete(wait=True)
        
        print(f"Instance deleted: {instance_name}")
        
        # List all instances
        instances = await client.instances.list()
        print(f"Remaining instances: {len(instances)}")
        for instance in instances:
            print(f"  {instance.name} ({instance.type}): {instance.status}")


if __name__ == "__main__":
    asyncio.run(main())
