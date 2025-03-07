# Incus Python SDK Documentation

Welcome to the Incus Python SDK documentation. This SDK provides a Python interface to the Incus REST API, allowing you to manage Incus containers, virtual machines, networks, storage pools, and more.

## Contents

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [API Reference](api/index.md)
- [Examples](examples.md)
- [Error Handling](error_handling.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)

## Overview

The Incus Python SDK is a comprehensive client library for the Incus API. It provides:

- Asynchronous API support using Python's asyncio
- Object-oriented models for Incus resources
- Comprehensive error handling
- Support for Unix socket and HTTPS connections
- Project-based resource management

## Available API Clients

The SDK includes the following API clients:

- `InstancesAPI` - Manage containers and virtual machines
- `ImagesAPI` - Manage images
- `NetworksAPI` - Manage networks
- `ProfilesAPI` - Manage profiles
- `StoragePoolsAPI` - Manage storage pools and volumes
- `CertificatesAPI` - Manage certificates
- `ClusterAPI` - Manage clusters and cluster members
- `OperationsAPI` - Manage operations
- `ProjectsAPI` - Manage projects

## Quick Example

```python
import asyncio
from incus_sdk import Client

async def main():
    # Connect to the Incus API
    async with Client() as client:
        # List all instances
        instances = await client.instances.list()
        print(f"Found {len(instances)} instances:")
        
        for instance in instances:
            print(f"  {instance.name} ({instance.type}): {instance.status}")

if __name__ == "__main__":
    asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
