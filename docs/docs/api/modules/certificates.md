# Certificates API

The `CertificatesAPI` client provides methods for managing Incus certificates.

## Usage

```python
from incus_sdk import Client

async with Client() as client:
    # List all certificates
    certificates = await client.certificates.list()
    
    # Get a certificate by fingerprint
    certificate = await client.certificates.get("abcdef123456")
    
    # Create a new certificate
    with open("client.crt", "r") as f:
        cert_data = f.read()
    
    await client.certificates.create(
        certificate=cert_data,
        name="my-client",
        type="client",
        restricted=True,
        projects=["default"]
    )
    
    # Update a certificate
    await client.certificates.update(
        "abcdef123456",
        {
            "name": "updated-client",
            "restricted": False
        }
    )
    
    # Delete a certificate
    await client.certificates.delete("abcdef123456")
```

## Class Documentation

::: incus_sdk.api.certificates.CertificatesAPI
    options:
      show_root_heading: false
      show_source: true

## Methods

### list

```python
async def list(recursion: int = 1) -> List[Certificate]
```

List all certificates.

**Parameters:**
- `recursion`: Level of recursion for the response (default: 1).

**Returns:**
- A list of `Certificate` objects.

### get

```python
async def get(fingerprint: str) -> Certificate
```

Get a certificate by fingerprint.

**Parameters:**
- `fingerprint`: Fingerprint of the certificate.

**Returns:**
- A `Certificate` object.

### create

```python
async def create(
    certificate: str,
    name: str = None,
    type: str = "client",
    restricted: bool = False,
    projects: List[str] = None,
    password: str = None,
) -> Dict[str, Any]
```

Create a new certificate.

**Parameters:**
- `certificate`: Certificate data as a string.
- `name`: Name of the certificate (optional).
- `type`: Type of certificate (default: "client").
- `restricted`: Whether the certificate is restricted (default: False).
- `projects`: List of projects the certificate has access to (optional).
- `password`: Password for the certificate (optional).

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Create a client certificate
with open("client.crt", "r") as f:
    cert_data = f.read()

await client.certificates.create(
    certificate=cert_data,
    name="my-client",
    type="client",
    restricted=True,
    projects=["default", "production"]
)
```

### delete

```python
async def delete(
    fingerprint: str
) -> Dict[str, Any]
```

Delete a certificate.

**Parameters:**
- `fingerprint`: Fingerprint of the certificate.

**Returns:**
- The operation response as a dictionary.

### update

```python
async def update(
    fingerprint: str, 
    data: Dict[str, Any]
) -> Dict[str, Any]
```

Update a certificate.

**Parameters:**
- `fingerprint`: Fingerprint of the certificate.
- `data`: New certificate data as a dictionary.

**Returns:**
- The operation response as a dictionary.

**Example:**

```python
# Update a certificate
await client.certificates.update(
    "abcdef123456",
    {
        "name": "updated-client",
        "restricted": False,
        "projects": ["default", "staging", "production"]
    }
)
```
