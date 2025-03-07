#!/usr/bin/env python3
"""
Advanced usage example for the Incus Python SDK.

This example demonstrates how to use multiple API clients together.
"""

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
