# Incus Python SDK

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://orbical-dev.github.io/incus_sdk/)
[![PyPI version](https://img.shields.io/pypi/v/incus-sdk.svg)](https://pypi.org/project/incus-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/incus-sdk.svg)](https://pypi.org/project/incus-sdk/)

A Python SDK for interacting with the Incus API. This SDK provides a simple and intuitive way to manage Incus containers, virtual machines, and other resources using Python.

## Installation

```bash
pip install incus-sdk
```

## Documentation

Comprehensive documentation is available at [https://orbical-dev.github.io/incus_sdk/](https://orbical-dev.github.io/incus_sdk/)

The documentation includes:
- Installation instructions
- Quick start guide
- API reference
- Code examples
- Error handling guide
- Contributing guidelines

### Local Development

To build and view the documentation locally:

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build and serve the documentation
cd docs
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.

## Features

- Full support for Incus REST API
- Asynchronous operation support
- Easy management of containers, virtual machines, networks, profiles, storage pools, and clusters
- Certificate-based authentication
- Support for local and remote Incus servers
- Comprehensive error handling with specific exception types
- Project-based resource management

## Quick Start

```python
from incus_sdk import Client

# Connect to local Incus socket
client = Client()

# List all instances
instances = client.instances.list()
for instance in instances:
    print(f"Instance: {instance.name}, Status: {instance.status}")

# Create a new container
container = client.instances.create(
    name="my-container",
    source={
        "type": "image",
        "protocol": "simplestreams",
        "server": "https://images.linuxcontainers.org",
        "alias": "ubuntu/22.04"
    },
    wait=True
)

# Start the container
container.start(wait=True)

# Create a network
network = client.networks.create(
    name="my-network",
    config={
        "ipv4.address": "10.0.0.1/24",
        "ipv4.nat": "true"
    }
)

# Error handling
try:
    instance = client.instances.get("non-existent")
except incus_sdk.IncusNotFoundError as e:
    print(f"Instance not found: {e}")
```

## Documentation

For detailed documentation, visit [https://incus-sdk.readthedocs.io](https://incus-sdk.readthedocs.io)

## Available API Clients

The SDK provides the following API clients:

- `instances` - Manage containers and virtual machines
- `images` - Manage images and aliases
- `networks` - Manage networks
- `profiles` - Manage profiles
- `storage_pools` - Manage storage pools and volumes
- `certificates` - Manage certificates
- `operations` - Manage operations
- `projects` - Manage projects
- `cluster` - Manage clusters and cluster members

## Error Handling

The SDK provides specific exception types for different error scenarios:

- `IncusError` - Base exception for all Incus errors
- `IncusAPIError` - Exception for API request failures
- `IncusConnectionError` - Exception for connection failures
- `IncusOperationError` - Exception for operation failures
- `IncusNotFoundError` - Exception for resource not found errors
- `IncusAuthenticationError` - Exception for authentication failures
- `IncusPermissionError` - Exception for permission denied errors

## License

MIT License