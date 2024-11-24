"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
import datetime

from app.utils.settings.config import settings


def c_config_query(config_definition_key: str, config_key: str, data: dict) -> tuple:
    """
    Insert a new configuration in the configuration table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.
    data: dict
        The data for the configuration.

    -- Returns
    str
        The SQL query to insert the configuration.
    """

    data_str = json.dumps(data)
    created_at = datetime.datetime.now()
    modified_at = datetime.datetime.now()

    query = f"""
    INSERT INTO {config_definition_key} (config_key, data, created_at, modified_at)
    VALUES (%s, %s, %s, %s);
    """

    return query, (
        config_key,
        data_str,
        created_at,
        modified_at,
    )


def r_config_query(config_definition_key: str, config_key: str) -> tuple:
    """
    Retrieve a configuration from the configuration table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.

    -- Returns
    str
        The SQL query to retrieve the configuration.
    """

    query = f"""
    SELECT
    config_key,
    data AS config_data,
    created_at,
    modified_at

    FROM {config_definition_key}
    WHERE config_key = %s
    LIMIT 1;
    """

    return query, (config_key,)


def u_config_query(config_definition_key: str, config_key: str, data: dict) -> tuple:
    """
    Update an existing configuration in the configuration table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration to be updated.
    data: dict
        The updated data for the configuration.

    -- Returns
    tuple
        The SQL query and its parameters to update the configuration.
    """

    data_str = json.dumps(data)
    modified_at = datetime.datetime.now()

    query = f"""
    UPDATE {config_definition_key}
    SET data = %s, modified_at = %s
    WHERE config_key = %s;
    """

    return query, (
        data_str,
        modified_at,
        config_key,
    )


def d_config_query(config_definition_key: str, config_key: str) -> tuple:
    """
    Delete a configuration from the configuration table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.

    -- Returns
    str
        The SQL query to delete the configuration.
    """

    query = f"""
    DELETE FROM {config_definition_key}
    WHERE config_key = %s;
    """

    return query, (config_key,)


def l_config_query(
    config_definition_key: str, page: int = 1, page_size: int = 10
) -> tuple:
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
    str
        The SQL query to list the configurations.
    """

    query = f"""
    SELECT 
    config_key,
    data AS config_data,
    created_at,
    modified_at

    FROM {config_definition_key}
    LIMIT %s OFFSET %s;
    """

    offset = page_size * (page - 1)
    return query, (page_size, offset)
