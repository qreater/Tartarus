"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.configs.queries import c_config_query, d_config_query

from app.utils.configs.validations import (
    validate_config_creation,
    validate_config_deletion,
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

    if rows_affected == 0:
        raise ValueError("Configuration not found.")

    return None
