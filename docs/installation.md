# Installation

The Incus Python SDK can be installed using pip:

```bash
pip install incus_sdk
```

## Requirements

* Python 3.7 or higher
* aiohttp 3.8.0 or higher
* certifi 2021.10.8 or higher
* aiofiles 0.8.0 or higher

## Installing from Source

You can also install the SDK from source:

```bash
git clone https://github.com/orbical-dev/incus_sdk.git
cd incus_sdk
pip install -e .
```

This will install the SDK in development mode, allowing you to make changes to the code and have them immediately reflected in your environment.

## Development Installation

For development, you can install additional dependencies:

```bash
pip install -e ".[dev]"
```

This will install development dependencies such as:

* pytest
* flake8
* black
* mypy
* sphinx (for documentation)
