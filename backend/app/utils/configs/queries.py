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
