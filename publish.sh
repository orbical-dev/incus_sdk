#!/bin/bash
# Script to build and upload the incus_sdk package to PyPI

set -e  # Exit immediately if a command exits with a non-zero status

# Display script banner
echo "====================================================="
echo "   Incus SDK PyPI Publishing Script"
echo "====================================================="
echo

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "Error: twine is not installed. Installing..."
    pip install twine
fi

# Check if build is installed
if ! command -v build &> /dev/null; then
    echo "Error: build is not installed. Installing..."
    pip install build
fi

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "Building the package..."
python -m build

# Verify the built package
echo "Verifying the package..."
twine check dist/*

# Ask for PyPI credentials
echo
echo "PyPI Upload"
echo "==========="
echo "You'll need your PyPI username and password to upload the package."
echo "If you haven't created a PyPI account, please do so at https://pypi.org/account/register/"
echo

# Ask if user wants to upload to TestPyPI first
read -p "Do you want to upload to TestPyPI first? (recommended) [y/N]: " test_pypi
if [[ $test_pypi =~ ^[Yy]$ ]]; then
    echo "Uploading to TestPyPI..."
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    
    echo
    echo "Package uploaded to TestPyPI!"
    echo "You can install it using:"
    echo "pip install --index-url https://test.pypi.org/simple/ incus_sdk"
    echo
    
    # Ask if user wants to continue with PyPI upload
    read -p "Do you want to proceed with uploading to PyPI? [y/N]: " proceed
    if [[ ! $proceed =~ ^[Yy]$ ]]; then
        echo "Upload to PyPI aborted."
        exit 0
    fi
fi

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo
echo "====================================================="
echo "   Package successfully uploaded to PyPI!"
echo "====================================================="
echo "You can now install it using:"
echo "pip install incus_sdk"
echo
echo "Don't forget to create a git tag for this release:"
echo "git tag -a v$(grep -m 1 version setup.py | cut -d '\"' -f 2) -m \"Release v$(grep -m 1 version setup.py | cut -d '\"' -f 2)\""
echo "git push origin v$(grep -m 1 version setup.py | cut -d '\"' -f 2)"
