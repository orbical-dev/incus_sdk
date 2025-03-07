#!/usr/bin/env python3
"""
Tests for the Incus Python SDK client.
"""

import asyncio
import os
import sys
import unittest

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incus_sdk import Client
from incus_sdk.exceptions import IncusNotFoundError


class TestClient(unittest.TestCase):
    """Test the Incus client."""

    def setUp(self):
        """Set up the test."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = Client()

    def tearDown(self):
        """Tear down the test."""
        self.loop.run_until_complete(self.client.disconnect())
        self.loop.close()

    def test_connect(self):
        """Test connecting to the Incus API."""
        self.loop.run_until_complete(self.client.connect())
        self.assertIsNotNone(self.client.api._session)

    def test_get_server_info(self):
        """Test getting server information."""
        self.loop.run_until_complete(self.client.connect())
        info = self.loop.run_until_complete(self.client.get_server_info())
        self.assertIsNotNone(info)
        self.assertIn("metadata", info)
        self.assertIn("api_version", info["metadata"])

    def test_get_resources(self):
        """Test getting server resources."""
        self.loop.run_until_complete(self.client.connect())
        resources = self.loop.run_until_complete(self.client.get_resources())
        self.assertIsNotNone(resources)
        self.assertIn("metadata", resources)
        self.assertIn("cpu", resources["metadata"])
        self.assertIn("memory", resources["metadata"])

    def test_list_instances(self):
        """Test listing instances."""
        self.loop.run_until_complete(self.client.connect())
        instances = self.loop.run_until_complete(self.client.instances.list())
        self.assertIsNotNone(instances)
        self.assertIsInstance(instances, list)

    def test_get_nonexistent_instance(self):
        """Test getting a non-existent instance."""
        self.loop.run_until_complete(self.client.connect())
        with self.assertRaises(IncusNotFoundError):
            self.loop.run_until_complete(self.client.instances.get("nonexistent-instance"))

    def test_list_images(self):
        """Test listing images."""
        self.loop.run_until_complete(self.client.connect())
        images = self.loop.run_until_complete(self.client.images.list())
        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)

    def test_list_networks(self):
        """Test listing networks."""
        self.loop.run_until_complete(self.client.connect())
        networks = self.loop.run_until_complete(self.client.networks.list())
        self.assertIsNotNone(networks)
        self.assertIsInstance(networks, list)

    def test_list_profiles(self):
        """Test listing profiles."""
        self.loop.run_until_complete(self.client.connect())
        profiles = self.loop.run_until_complete(self.client.profiles.list())
        self.assertIsNotNone(profiles)
        self.assertIsInstance(profiles, list)

    def test_list_storage_pools(self):
        """Test listing storage pools."""
        self.loop.run_until_complete(self.client.connect())
        pools = self.loop.run_until_complete(self.client.storage_pools.list())
        self.assertIsNotNone(pools)
        self.assertIsInstance(pools, list)

    def test_list_operations(self):
        """Test listing operations."""
        self.loop.run_until_complete(self.client.connect())
        operations = self.loop.run_until_complete(self.client.operations.list())
        self.assertIsNotNone(operations)
        self.assertIsInstance(operations, list)


if __name__ == "__main__":
    unittest.main()
