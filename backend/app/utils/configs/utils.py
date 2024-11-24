"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.configs.queries import (
    c_config_query,
    r_config_query,
    d_config_query,
    l_config_query,
    u_config_query,
)

from app.utils.configs.validations import (
    validate_config_creation,
    validate_config_read,
    validate_config_deletion,
    validate_config_list,
    validate_config_update,
)

from app.utils.data.data_source import DataStore

data_store = DataStore()


def c_config(config_definition_key: str, config_key: str, data: dict):
    """
    Create a new configuration for the configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.
    data: dict
        The data for the configuration.
    """

    validate_config_creation(config_definition_key, config_key, data)

    creation_query, creation_params = c_config_query(
        config_definition_key, config_key, data
    )
    data_store.execute_query(creation_query, creation_params)

    return None


def r_config(config_definition_key: str, config_key: str):
    """
    Retrieve a configuration from the configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.

    -- Returns
    dict
        The configuration data.
    """

    validate_config_read(config_definition_key, config_key)

    query, params = r_config_query(config_definition_key, config_key)
    result = data_store.execute_query(query, params=params, mode="retrieve")["response"]

    if len(result) == 0 or result is None:
        raise ValueError("Configuration not found.")

    return result[0]


def u_config(config_definition_key: str, config_key: str, data: dict):
    """
    Update an existing configuration for the configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration to be updated.
    data: dict
        The updated data for the configuration.
    """

    validate_config_update(config_definition_key, config_key, data)

    update_query, update_params = u_config_query(
        config_definition_key, config_key, data
    )
    rows_affected = data_store.execute_query(update_query, update_params)[
        "rows_affected"
    ]

    if rows_affected != 1:
        raise ValueError(f"Configuration with key '{config_key}' not found.")

    return None


def d_config(config_definition_key: str, config_key: str):
    """
    Delete a configuration from the configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.
    """

    validate_config_deletion(config_definition_key, config_key)

    deletion_query, deletion_params = d_config_query(config_definition_key, config_key)
    rows_affected = data_store.execute_query(deletion_query, deletion_params)[
        "rows_affected"
    ]

    if rows_affected != 1:
        raise ValueError("Configuration not found.")

    return None


def l_config(config_definition_key: str, page: int = 1, page_size: int = 10):
    """
    List all configurations for a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    page: int, optional
        The page number. Defaults to 1.
    page_size: int, optional
        The number of configurations to list per page. Defaults to 10.

    -- Returns
    list
        The configurations.
    """

    validate_config_list(config_definition_key, page, page_size)

    query, params = l_config_query(config_definition_key, page, page_size)
    result = data_store.execute_query(query, params=params, mode="retrieve")["response"]

    return result
