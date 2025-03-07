#!/usr/bin/env python3
"""
Comprehensive example for the Incus Python SDK.

This example demonstrates how to use various features of the SDK.
"""

import asyncio
import os
import sys
import json

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client


async def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)


async def main():
    """Main function."""
    # Connect to the Incus API
    async with Client() as client:
        # Get server info
        await print_section("Server Information")
        server_info = await client.get_server_info()
        print(f"API version: {server_info.get('metadata', {}).get('api_version')}")
        print(f"API status: {server_info.get('metadata', {}).get('api_status')}")
        print(f"Auth methods: {', '.join(server_info.get('metadata', {}).get('auth_methods', []))}")

        # Get server resources
        await print_section("Server Resources")
        resources = await client.get_resources()
        print(f"CPU: {resources.get('metadata', {}).get('cpu', {}).get('total')} cores")
        print(f"Memory: {resources.get('metadata', {}).get('memory', {}).get('total')} bytes")
        print(f"Storage: {resources.get('metadata', {}).get('storage', {}).get('total')} bytes")

        # List instances
        await print_section("Instances")
        instances = await client.instances.list()
        print(f"Found {len(instances)} instances:")
        for instance in instances:
            print(f"  {instance.name} ({instance.type}): {instance.status}")

        # List images
        await print_section("Images")
        images = await client.images.list()
        print(f"Found {len(images)} images:")
        for image in images:
            aliases = [alias.name for alias in image.aliases]
            alias_str = f" ({', '.join(aliases)})" if aliases else ""
            print(f"  {image.fingerprint[:12]}{alias_str}: {image.properties.get('description', 'No description')}")

        # List profiles
        await print_section("Profiles")
        profiles = await client.profiles.list()
        print(f"Found {len(profiles)} profiles:")
        for profile in profiles:
            print(f"  {profile.name}: {profile.description or 'No description'}")

        # List networks
        await print_section("Networks")
        networks = await client.networks.list()
        print(f"Found {len(networks)} networks:")
        for network in networks:
            print(f"  {network.name} ({network.type}): {network.description or 'No description'}")

        # List storage pools
        await print_section("Storage Pools")
        pools = await client.storage_pools.list()
        print(f"Found {len(pools)} storage pools:")
        for pool in pools:
            print(f"  {pool.name} ({pool.driver}): {pool.description or 'No description'}")

        # List projects
        await print_section("Projects")
        projects = await client.projects.list()
        print(f"Found {len(projects)} projects:")
        for project in projects:
            print(f"  {project.name}: {project.description or 'No description'}")

        # Check if clustering is enabled
        await print_section("Cluster Information")
        cluster = await client.cluster.get()
        if cluster.enabled:
            print("Clustering is enabled")
            print(f"Found {len(cluster.members)} cluster members:")
            for member in cluster.members:
                print(f"  {member.server_name} ({member.status}): {member.message or 'No message'}")
        else:
            print("Clustering is not enabled")

        # List operations
        await print_section("Operations")
        operations = await client.operations.list()
        print(f"Found {len(operations)} operations:")
        for operation in operations:
            print(f"  {operation.get('id')}: {operation.get('description')} ({operation.get('status')})")


if __name__ == "__main__":
    asyncio.run(main())
