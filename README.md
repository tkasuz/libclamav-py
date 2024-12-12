# libclamav-py

libclamav-py is a Python wrapper for the ClamAV library, providing an interface to ClamAV's virus scanning capabilities.

## Features
- Directly invokes the C API of libclamav, so the clamd daemon doesn't need to be running on your machine
- Lambda Layer which libclamav is binded (TODO)

## Installation

To install libclamav-py, use pip:

```sh
pip install libclamav-py
```

## Usage

Here is a basic example of how to use libclamav-py:

```python
from libclamav_py.clamav import Client

# Initialize the libclamav engine with the default setting
client = Client(clamd_conf_path="/lib/libclamav.so")

# Or libclamav client can be initialized from clamd.conf
client = Client.from_clamd_conf(clamd_conf_path="/etc/clamd.conf", clamd_conf_path="/lib/libclamav.so")
```

```python
# Load virus definitions
client.load_db()

# Compile engine
client.compile_engine()

# Scan a file
result = client.scan_file('/path/to/file')
if result:
    print(f"Virus detected: {result}")
else:
    print("No virus detected")
```

## License
This project is licensed under the GPL-2.0 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [ClamAV](https://www.clamav.net/) for the virus scanning engine
