# Contributing

We welcome contributions to the Incus Python SDK! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:

   ```bash
   git clone https://github.com/orbical-dev/incus_sdk.git
   cd incus_sdk
   ```

3. Create a virtual environment and install the development dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. Create a branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

We follow the PEP 8 style guide for Python code. You can use tools like `flake8` and `black` to ensure your code adheres to our style guidelines:

```bash
flake8 incus_sdk
black incus_sdk
```

### Type Hints

We use type hints throughout the codebase. Please add appropriate type hints to your code:

```python
def example_function(param1: str, param2: int) -> bool:
    return True
```

### Documentation

Please document your code using docstrings. We follow the Google style for docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Example function that demonstrates docstring style.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: Description of when this error is raised.
    """
    return True
```

### Testing

Please add tests for your changes. We use `pytest` for testing:

```bash
pytest tests/
```

## Pull Request Process

1. Update the documentation if necessary.
2. Add or update tests as necessary.
3. Ensure your code passes all tests and style checks.
4. Submit a pull request to the main repository.
5. The pull request will be reviewed by the maintainers.
6. Once approved, your changes will be merged.

## Code of Conduct

Please be respectful and considerate of others when contributing to the project. We strive to maintain a welcoming and inclusive community.
