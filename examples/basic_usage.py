#!/usr/bin/env python3
"""
Basic usage example for the Incus Python SDK.
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client


async def main():
    """Main function."""
    # Connect to the Incus API
    async with Client(project="Orbical-Website") as client:
        # Get server info
        server_info = await client.get_server_info()
        print("Server info:")
        print(f"  API version: {server_info.get('metadata', {}).get('api_version')}")
        print(f"  API status: {server_info.get('metadata', {}).get('api_status')}")
        print(f"  Auth methods: {server_info.get('metadata', {}).get('auth_methods')}")
        print()

        # List instances
        instances = await client.instances.list()
        print(f"Found {len(instances)} instances:")
        for instance in instances:
            print(f"  {instance.name} ({instance.type}): {instance.status}")
        print()

        # List images
        images = await client.images.list()
        print(f"Found {len(images)} images:")
        for image in images:
            aliases = [alias.name for alias in image.aliases]
            alias_str = f" ({', '.join(aliases)})" if aliases else ""
            print(f"  {image.fingerprint[:12]}{alias_str}: {image.properties.get('description', 'No description')}")


if __name__ == "__main__":
    asyncio.run(main())
