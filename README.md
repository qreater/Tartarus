## Tartarus

![](/docs/assets/banner.webp)

Tartarus is your go-to solution for managing  configurations with security, flexibility, and scalability at its core. Engineered for modern software systems, it streamlines the storage and retrieval of configurations while ensuring robust data integrity.

## Contents

- [Tech Stack, Tools and Libraries](#tech-stack-tools-and-libraries)
- [DB and Design](#db-and-design)
- [API Documentation](#api-documentation)
- [Internal Table](#internal-table)
- [Configuration Definition Table](#configuration-definition-table)
- [Configurations](#configurations)
- [Setup & Environment](#setup)
- [Testing](#testing)
- [Continuous Integration and Deployment](#continuous-integration-and-deployment)
- [License](#license)

## Tech Stack, Tools and Libraries

### Backend

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [Poetry](https://python-poetry.org/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Psycopg2](https://www.psycopg.org/docs/)


### Devops

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Others

- [Visual Studio Code](https://visualstudio.microsoft.com/vs/code/)
- [Postman](https://www.postman.com/)
- [Git](https://git-scm.com/)


## DB and Design

Tartarus leverages `PostgreSQL` as its primary database, ensuring robust performance, reliability, and scalability. The database seamlessly integrates with the FastAPI application via the highly efficient `psycopg2` library, which provides low-level, optimized database interactions.

Tartarus employs a modular and well-structured database schema to efficiently manage application configurations. An [internal table](#internal-table) is deployed to maintain configuration definition details, where each [configuration definition](#configuration-definition-table) is associated with a dedicated table containing its [configurations](#configurations) as records, which form the backbone of this system, ensuring both flexibility and consistency.


### Connection and Execution

The [DataStore](/backend/app/utils/data/data_source.py) class is designed to manage the database connections and queries efficiently. It abstracts the database interactions, ensuring a clean, modular, and scalable codebase. The class manages all database connections through a single interface and supports broad range of queries with error handling.


## API Documentation

Swagger UI can be used to test the API. It is available at `/docs` route of the API Server. The API documentation provides a detailed overview of the available endpoints, request/response formats, and authentication mechanisms.


## Internal Table

The Internal table is designed to store and maintain the list of `config-definitions` used by the end-users. The Internal table schema includes the following columns:

- Configuration Key (`config_definition_key`): The unique identifier for the configuration key.
- JSON Value (`json_schema`): The JSON value associated with the configuration key.
- Indexes (`indexes`): The indexes associated with the configuration key.

## Configuration Definition Table

The Configuration Definition (`config_definition`) table acts as the blueprint for the `config`, defining the structure, constraints, and expected behavior of configuration keys. This separation ensures that all configurations adhere to predefined rules and maintain consistency across the application.


### Table Schema

Each Configuration Definition Table is named as `config_definition_key` and contains the following columns:

- Configuration Key (`config_key`): The unique identifier for the configuration key.
- JSON Schema (`data`): The JSON schema associated with the configuration key.
- Created At (`created_at`): The timestamp when the configuration key was created.
- Modified At (`modified_at`): The timestamp when the configuration key was last modified.


### Endpoints

The Configuration Definition Table provides the following endpoints:

| **Action**                      | **HTTP Method** | **Endpoint**                                |
|---------------------------------|-----------------|---------------------------------------------|
| Create Config Definition | POST            | `/config-definition/`                       |
| Get Config Definition    | GET             | `/config-definition/{config_definition_key}`|
| Update Config Definition | PUT             | `/config-definition/{config_definition_key}`|
| Delete Config Definition | DELETE          | `/config-definition/{config_definition_key}`|
| List Config Definitions  | GET             | `/config-definition/`                       |


## Configurations

The Configurations (`config`) stores the actual configuration values associated with the configuration keys defined in the `config_definition` table. The config table serves as the dynamic repository for storing runtime configuration details used by the application. Each entry in this table represents an individual configuration parameter, ensuring precise control over application behavior.


### Endpoints

The Configuration Table provides the following endpoints:

| **Action**                      | **HTTP Method** | **Endpoint**                                |
|---------------------------------|-----------------|---------------------------------------------|
| Create Config           | POST            | `/config_definition/{config_definition_key}/config/`                                  |
| Get Config               | GET             | `/config_definition/{config_definition_key}/config/{config_key}`                      |
| Update Config           | PUT             | `/config_definition/{config_definition_key}/config/{config_key}`                      |
| Delete Config            | DELETE          | `/config_definition/{config_definition_key}/config/{config_key}`                      |
| List Configs            | GET             | `/config_definition/{config_definition_key}/config/`                                  |



## Setup

To run the Tartarus application, follow these steps:

### Clone the repository

```bash
git clone https://www.github.com/qreater/tartarus.git
```

### Navigate to the project directory

```bash
cd backend
```

### Install the dependencies using Poetry

```bash
poetry install
```

### Start the FastAPI application

```bash
poetry run uvicorn app.main:app --reload --host 8000
```

[!NOTE]

Access the FastAPI application at `http://localhost:8000/docs`.


## Testing

The Tartarus application is thoroughly tested using the `pytest` framework, ensuring robustness, reliability, and consistency across all modules. The test suite covers unit tests, integration tests, and end-to-end tests, validating the functionality, performance, and security of the application.

The tests are organized into the following categories:

- [Unit Tests](backend/tests/unit_tests/): Test individual functions, methods, and classes in isolation.
- [Integration Tests](/backend/tests/integration_tests/): Test the interaction between different components, modules, and services.

The test suite is executed using the following command:

```bash
poetry run pytest
```

## Continuous Integration and Deployment

The Tartarus application is integrated with GitHub Actions to automate the testing, building, and deployment processes. The CI/CD pipeline ensures that the application is thoroughly tested, packaged, and deployed to the target environment seamlessly.

The CI/CD pipeline includes the following stages:

- **Style Check**: Run `black` to ensure code consistency and formatting.
- **Unit Tests**: Execute the unit tests to validate individual components.
- **Integration Tests**: Run the integration tests to validate the interaction between components.


## License
![](/docs/assets/license.webp)
Licensed under the Apache License, Version 2.0. See [License](/LICENSE) for more information.

