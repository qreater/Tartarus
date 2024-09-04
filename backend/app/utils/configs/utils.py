"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.configs.queries import (
    c_config_query,
)

from app.utils.configs.validations import (
    validate_config_creation,
)

from app.utils.data.data_source import DataStore

data_store = DataStore()


def c_config(config_definition_key: str, config_key: str, data: dict):
    """
    Create a new configuration for the config definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration type.
    config_key: str
        The key for the configuration.
    data: dict
        The data for the configuration.
    """

    validate_config_creation(config_definition_key, config_key, data)

    creation_query, creation_params = c_config_query(
        config_definition_key, config_key, data
    )
    data_store._execute_query(creation_query, creation_params)

    return None
