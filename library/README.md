# Tartarus-Lib: Python Client for Tartarus Config Store

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/tartarus-lib.svg)](https://badge.fury.io/py/tartarus-lib)
[![Build Status](https://img.shields.io/github/actions/workflow/status/qreater/tartarus/pypi-publish.yaml?branch=main)](https://github.com/qreater/tartarus/actions/workflows/pypi-publish.yaml)

Tartarus-Lib is a streamlined Python client designed for seamless interaction with the Tartarus Config Store API. It simplifies configuration management by providing intuitive methods for creating, retrieving, updating, and deleting configurations and their definitions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example Usage](#example-usage)
- [Error Handling](#error-handling)
- [License](#license)

## Installation

Install Tartarus-Lib using pip:

```bash
pip install tartarus-lib
```

## Usage

This section provides an overview of the Tartarus-Lib client and its usage. This requires a basic understanding of the Tartarus Config Store API. For more information, refer to the [Tartarus Config Store API Documentation](https://github.com/Qreater/tartarus/blob/main/README.md).

Once the API Server is up and running, you can use the Tartarus-Lib client to interact with the API endpoints. The client provides sub-clients for each of the API endpoints, allowing you to perform CRUDL operations on configurations and their definitions.

### Initialization

Import the TartarusAPIClient class and initialize it with the URL, API KEY of the Tartarus Config Store API:

```python
from tartarus_lib.core import TartarusAPIClient
```

```python
client = TartarusAPIClient(API_URL, API_KEY)
```

### Sub-Clients

Tartarus-Lib provides sub-clients for each of the API endpoints. These sub-clients can be accessed using the client object:

```python
config_definitions = client.config_definitions
```

```python
configs = client.configs
```

### Methods

Each sub-client provides methods for interacting with the corresponding API endpoint. The methods are designed to be intuitive and easy to use:

- `.create()`: Create a new configuration or definition
- `.retrieve()`: Retrieve an existing configuration or definition
- `.update()`: Update an existing configuration or definition
- `.delete()`: Delete an existing configuration or definition
- `.list()`: List configurations or definitions (Paginated)

## Example Usage

The following example demonstrates how to use the Tartarus-Lib client to interact with the Tartarus Config Store API:

Create a configuration definition. This step is necessary before creating a configuration. Please refer to the [Tartarus Config Store API Documentation](https://github.com/Qreater/tartarus/blob/main/README.md) for more information on configuration definitions:

```python
config_definitions.create(
    config_definition_key="test_config_definition",
)
```

Create a configuration using the definition key and the configuration key. The data parameter contains the configuration values:
```python
configs.create(
    config_definition_key="test_config_definition",
    config_key="test_config",
    data={
        "name": "Alice", 
        "age": 30
    },
)
```

Retrieve the configuration using the definition key and the configuration key:
```python
config = configs.retrieve(
    config_definition_key="test_config_definition",
    config_key="test_config"
)
```

Delete the configuration using the definition key and the configuration key:
```python
configs.delete(
    config_definition_key="test_config_definition",
    config_key="test_config"
)
```


## Error Handling

Tartarus-Lib raises TartarusError exceptions for any errors that occur during API requests. You can catch these exceptions and handle them accordingly:

```python
from tartarus_lib.core import TartarusError

try:
    '''
    Perform API operations here
    '''
except TartarusError as e:
    '''
    Handle the error here
    '''
```


## License

Tartarus-Lib is licensed under the Apache License 2.0. See [LICENSE](../LICENSE) for more information.


