from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="incus_sdk",
    version="1.0.0",
    author="Incus SDK Team",
    author_email="zacharyj@orbical.dev",
    description="A Python SDK for the Incus API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orbical-dev/incus_sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "certifi>=2021.10.8",
        "aiofiles>=0.8.0",
    ],
)
