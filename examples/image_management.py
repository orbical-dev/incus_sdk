#!/usr/bin/env python3
"""
Image management example for the Incus Python SDK.

This example demonstrates how to manage images.
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
        # List all images
        images = await client.images.list()
        print(f"Found {len(images)} images:")
        for image in images:
            aliases = [alias.name for alias in image.aliases]
            alias_str = f" ({', '.join(aliases)})" if aliases else ""
            print(f"  {image.fingerprint[:12]}{alias_str}: {image.properties.get('description', 'No description')}")
        
        # Find an Ubuntu image
        ubuntu_image = None
        for image in images:
            for alias in image.aliases:
                if "ubuntu" in alias.name.lower():
                    ubuntu_image = image
                    break
            if ubuntu_image:
                break
        
        if not ubuntu_image:
            print("No Ubuntu image found. Please import an Ubuntu image first.")
            return
        
        print(f"\nFound Ubuntu image: {ubuntu_image.fingerprint[:12]}")
        
        # Create a new alias for the Ubuntu image
        alias_name = f"test-alias-{int(time.time())}"
        print(f"Creating alias: {alias_name}")
        
        response = await client.images.create_alias(
            name=alias_name,
            target=ubuntu_image.fingerprint,
            description="Test alias created by Incus Python SDK"
        )
        
        print(f"Alias created: {alias_name}")
        
        # Get the image with the new alias
        images = await client.images.list()
        for image in images:
            for alias in image.aliases:
                if alias.name == alias_name:
                    print(f"Found image with alias {alias_name}: {image.fingerprint[:12]}")
                    
                    # Print image details
                    print(f"Image details:")
                    print(f"  Fingerprint: {image.fingerprint}")
                    print(f"  Architecture: {image.architecture}")
                    print(f"  Size: {image.size} bytes")
                    print(f"  Type: {image.type}")
                    print(f"  Properties: {image.properties}")
                    break
        
        # Delete the alias
        print(f"Deleting alias: {alias_name}")
        await client.images.delete_alias(alias_name)
        print(f"Alias deleted: {alias_name}")


if __name__ == "__main__":
    asyncio.run(main())
