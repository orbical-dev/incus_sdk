# Models

The Incus Python SDK provides model classes for representing Incus resources. These models provide methods for interacting with the resources they represent.

## Base Model

All model classes in the Incus Python SDK inherit from the base `Model` class, which provides common functionality for all models.

```python
from incus_sdk.models.base import Model

# Create a model instance from a dictionary
data = {"name": "example", "description": "An example resource"}
model = Model.from_dict(data)

# Convert a model to a dictionary
data_dict = model.to_dict()
```

### Base Model Methods

- `to_dict()` - Convert the model to a dictionary.
- `from_dict(data, client=None)` - Create a model instance from a dictionary.

## Instance Model

The `Instance` model represents an Incus instance (container or virtual machine).

```python
from incus_sdk import Client

async with Client() as client:
    # Get an instance
    instance = await client.instances.get("my-instance")
    
    # Start the instance
    await instance.start()
    
    # Execute a command in the instance
    result = await instance.execute(["echo", "Hello, World!"])
    
    # Stop the instance
    await instance.stop()
    
    # Delete the instance
    await instance.delete()
```

### Instance Properties

- `name` - The name of the instance.
- `description` - The description of the instance.
- `type` - The type of the instance (container or virtual machine).
- `status` - The current status of the instance.
- `config` - The configuration of the instance.
- `devices` - The devices attached to the instance.
- `profiles` - The profiles applied to the instance.
- `state` - The current state of the instance.

### Instance Methods

- `async start(wait=False)` - Start the instance.
- `async stop(wait=False)` - Stop the instance.
- `async restart(wait=False)` - Restart the instance.
- `async freeze(wait=False)` - Freeze the instance.
- `async unfreeze(wait=False)` - Unfreeze the instance.
- `async delete(wait=False)` - Delete the instance.
- `async update(description=None, config=None, devices=None, profiles=None)` - Update the instance.
- `async execute(command, environment=None, wait_for_websocket=False, record_output=False, interactive=False, width=None, height=None, wait=False)` - Execute a command in the instance.
- `async get_state()` - Get the current state of the instance.
- `async get_logs()` - Get the logs of the instance.
- `async get_files(path)` - Get files from the instance.
- `async put_files(path, content)` - Put files into the instance.

## Image Model

The `Image` model represents an Incus image.

```python
from incus_sdk import Client

async with Client() as client:
    # Get an image
    image = await client.images.get("my-image")
    
    # Update the image properties
    await image.update(properties={"description": "My updated image"})
    
    # Delete the image
    await image.delete()
```

### Image Properties

- `fingerprint` - The fingerprint of the image.
- `filename` - The filename of the image.
- `size` - The size of the image.
- `architecture` - The architecture of the image.
- `public` - Whether the image is public.
- `properties` - The properties of the image.
- `aliases` - The aliases of the image.
- `auto_update` - Whether the image is auto-updated.
- `cached` - Whether the image is cached.

### Image Methods

- `async update(properties=None, public=None, auto_update=None)` - Update the image.
- `async delete()` - Delete the image.
- `async add_alias(name, description=None)` - Add an alias to the image.
- `async remove_alias(name)` - Remove an alias from the image.
- `async export(target_path)` - Export the image to a file.

## Network Model

The `Network` model represents an Incus network.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a network
    network = await client.networks.get("my-network")
    
    # Update the network
    await network.update(description="My updated network")
    
    # Delete the network
    await network.delete()
```

### Network Properties

- `name` - The name of the network.
- `description` - The description of the network.
- `type` - The type of the network.
- `config` - The configuration of the network.
- `managed` - Whether the network is managed.
- `status` - The current status of the network.

### Network Methods

- `async update(description=None, config=None)` - Update the network.
- `async delete()` - Delete the network.
- `async get_state()` - Get the current state of the network.
- `async get_leases()` - Get the DHCP leases of the network.

## Profile Model

The `Profile` model represents an Incus profile.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a profile
    profile = await client.profiles.get("my-profile")
    
    # Update the profile
    await profile.update(description="My updated profile")
    
    # Delete the profile
    await profile.delete()
```

### Profile Properties

- `name` - The name of the profile.
- `description` - The description of the profile.
- `config` - The configuration of the profile.
- `devices` - The devices defined in the profile.
- `used_by` - The instances using the profile.

### Profile Methods

- `async update(description=None, config=None, devices=None)` - Update the profile.
- `async delete()` - Delete the profile.

## StoragePool Model

The `StoragePool` model represents an Incus storage pool.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a storage pool
    pool = await client.storage_pools.get("my-pool")
    
    # Update the storage pool
    await pool.update(description="My updated storage pool")
    
    # Delete the storage pool
    await pool.delete()
```

### StoragePool Properties

- `name` - The name of the storage pool.
- `description` - The description of the storage pool.
- `driver` - The driver of the storage pool.
- `config` - The configuration of the storage pool.
- `status` - The current status of the storage pool.
- `resources` - The resources of the storage pool.

### StoragePool Methods

- `async update(description=None, config=None)` - Update the storage pool.
- `async delete()` - Delete the storage pool.
- `async list_volumes()` - List all volumes in the storage pool.
- `async create_volume(name, description=None, config=None, content_type=None)` - Create a new volume in the storage pool.
- `async get_volume(name)` - Get a volume from the storage pool.
- `async delete_volume(name)` - Delete a volume from the storage pool.

## Certificate Model

The `Certificate` model represents an Incus certificate.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a certificate
    certificate = await client.certificates.get("abcdef123456")
    
    # Update the certificate
    await certificate.update(
        name="updated-cert",
        restricted=True,
        projects=["default", "production"]
    )
    
    # Delete the certificate
    await certificate.delete()
```

### Certificate Properties

- `fingerprint` - The fingerprint of the certificate.
- `certificate` - The certificate data.
- `name` - The name of the certificate.
- `type` - The type of certificate (e.g., client).
- `restricted` - Whether the certificate is restricted.
- `projects` - List of projects the certificate has access to.

### Certificate Methods

- `async update(name=None, type=None, restricted=None, projects=None)` - Update the certificate.
- `async delete()` - Delete the certificate.

## Cluster Model

The `Cluster` model represents an Incus cluster.

```python
from incus_sdk import Client

async with Client() as client:
    # Get the cluster
    cluster = await client.cluster.get()
    
    # Add a new member to the cluster
    await cluster.add_member(
        name="node2",
        url="10.0.0.2:8443",
        config={"enabled": True}
    )
    
    # Get a cluster member
    member = await cluster.get_member("node2")
```

### Cluster Properties

- `enabled` - Whether clustering is enabled.
- `member_config` - Configuration for cluster members.
- `members` - List of cluster members.

### Cluster Methods

- `async get_member(name)` - Get a cluster member by name.
- `async add_member(name, url, config=None)` - Add a new member to the cluster.

## ClusterMember Model

The `ClusterMember` model represents a member of an Incus cluster.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a cluster member
    member = await client.cluster.get_member("node1")
    
    # Update the cluster member
    await member.update({"config": {"enabled": False}})
    
    # Delete the cluster member
    await member.delete()
```

### ClusterMember Properties

- `server_name` - The name of the cluster member.
- `url` - The URL of the cluster member.
- `database` - Whether the member is a database node.
- `status` - The current status of the cluster member.
- `message` - Status message.
- `architecture` - The architecture of the cluster member.
- `failure_domain` - The failure domain of the cluster member.
- `description` - The description of the cluster member.
- `config` - The configuration of the cluster member.
- `roles` - The roles of the cluster member.

### ClusterMember Methods

- `async update(config)` - Update the cluster member configuration.
- `async delete()` - Delete the cluster member.

## Project Model

The `Project` model represents an Incus project.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a project
    project = await client.projects.get("my-project")
    
    # Update the project
    await project.update({
        "description": "Updated project",
        "config": {"features.networks": "true"}
    })
    
    # Rename the project
    await project.rename("new-project-name")
    
    # Delete the project
    await project.delete()
```

### Project Properties

- `name` - The name of the project.
- `description` - The description of the project.
- `config` - The configuration of the project.
- `used_by` - List of resources using this project.

### Project Methods

- `async update(config)` - Update the project configuration.
- `async delete()` - Delete the project.
- `async rename(new_name)` - Rename the project.

## StorageVolume Model

The `StorageVolume` model represents a volume in an Incus storage pool.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a storage volume
    volume = await client.storage_pools.get_volume("my-pool", "my-volume")
    
    # Update the storage volume
    await volume.update(description="My updated storage volume")
    
    # Delete the storage volume
    await volume.delete()
```

### StorageVolume Properties

- `name` - The name of the storage volume.
- `description` - The description of the storage volume.
- `type` - The type of the storage volume.
- `content_type` - The content type of the storage volume.
- `config` - The configuration of the storage volume.
- `location` - The location of the storage volume.
- `used_by` - The instances using the storage volume.

### StorageVolume Methods

- `async update(description=None, config=None)` - Update the storage volume.
- `async delete()` - Delete the storage volume.
- `async resize(size)` - Resize the storage volume.
- `async snapshot(name, expiry=None)` - Create a snapshot of the storage volume.
- `async restore(snapshot)` - Restore a snapshot of the storage volume.
- `async delete_snapshot(snapshot)` - Delete a snapshot of the storage volume.

## Project Model

The `Project` model represents an Incus project.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a project
    project = await client.projects.get("my-project")
    
    # Update the project
    await project.update(description="My updated project")
    
    # Delete the project
    await project.delete()
```

### Project Properties

- `name` - The name of the project.
- `description` - The description of the project.
- `config` - The configuration of the project.
- `used_by` - The resources using the project.

### Project Methods

- `async update(description=None, config=None)` - Update the project.
- `async delete()` - Delete the project.

## Cluster Model

The `Cluster` model represents an Incus cluster.

```python
from incus_sdk import Client

async with Client() as client:
    # Get the cluster
    cluster = await client.cluster.get()
    
    # Update the cluster
    await cluster.update(description="My updated cluster")
```

### Cluster Properties

- `name` - The name of the cluster.
- `description` - The description of the cluster.
- `config` - The configuration of the cluster.
- `enabled` - Whether the cluster is enabled.
- `member_count` - The number of members in the cluster.

### Cluster Methods

- `async update(description=None, config=None)` - Update the cluster.
- `async list_members()` - List all members in the cluster.
- `async get_member(name)` - Get a member from the cluster.
- `async remove_member(name)` - Remove a member from the cluster.

## ClusterMember Model

The `ClusterMember` model represents a member of an Incus cluster.

```python
from incus_sdk import Client

async with Client() as client:
    # Get a cluster member
    member = await client.cluster.get_member("member1")
    
    # Update the cluster member
    await member.update(description="My updated cluster member")
    
    # Delete the cluster member
    await member.delete()
```

### ClusterMember Properties

- `name` - The name of the cluster member.
- `description` - The description of the cluster member.
- `url` - The URL of the cluster member.
- `database` - Whether the cluster member is a database node.
- `status` - The current status of the cluster member.
- `message` - The current message of the cluster member.

### ClusterMember Methods

- `async update(description=None)` - Update the cluster member.
- `async delete()` - Delete the cluster member.
