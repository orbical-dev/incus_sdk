#!/bin/bash
# Script to build the documentation for the Incus Python SDK

# Install MkDocs and required plugins if not already installed
pip install mkdocs mkdocstrings pymdown-extensions

# Build the documentation
mkdocs build

echo "Documentation built successfully in the 'site' directory."
echo "To view the documentation, run 'mkdocs serve' and open http://127.0.0.1:8000 in your browser."
