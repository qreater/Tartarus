"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.settings.config import settings
import json


def internal_c_definition_query(
    config_definition_key: str, json_schema: dict, indexes: list
) -> tuple:
    """
    Insert a new configuration definition in the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    indexes: list
        The indexes for the configuration definition.

    -- Returns
    str
        The SQL query to insert the configuration definition.
    """
    json_schema_str = json.dumps(json_schema)
    indexes_str = "{" + ",".join(f'"{item}"' for item in indexes) + "}"

    internal_query = f"""
    INSERT INTO {settings.INTERNAL_TABLE} (config_definition_key, json_schema, indexes)
    VALUES (%s, %s, %s);
    """

    return internal_query, (
        config_definition_key,
        json_schema_str,
        indexes_str,
    )


def internal_u_definition_query(config_definition_key: str, indexes: list) -> tuple:
    """
    Update a configuration definition in the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    indexes: list
        The indexes for the configuration definition.

    -- Returns
    tuple
        The SQL query to update the configuration definition and the parameters.
    """
    indexes = "{" + ",".join(f'"{item}"' for item in indexes) + "}"

    update_query = f"""
    UPDATE {settings.INTERNAL_TABLE}
    SET indexes = %s
    WHERE config_definition_key = %s;
    """

    return update_query, (
        indexes,
        config_definition_key,
    )


def internal_d_definition_query(config_definition_key: str) -> tuple:
    """
    Delete a configuration definition from the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    tuple
        The SQL query to delete the configuration definition and the parameters.
    """
    delete_query = f"""
    DELETE FROM {settings.INTERNAL_TABLE}
    WHERE config_definition_key = %s;
    """

    return delete_query, (config_definition_key,)


def c_index_query(config_definition_key: str, index: str) -> tuple:
    """
    Create an index on a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    index: str
        The index to create.

    -- Returns
    tuple
        The SQL query to create the index and the parameters.
    """
    index_query = f"""
    CREATE INDEX IF NOT EXISTS idx_{config_definition_key}_{index.replace('.', '_')}
    ON {config_definition_key} USING gin ((data->%s));
    """

    return index_query, (index,)


def d_index_query(config_definition_key: str, index: str) -> tuple:
    """
    Remove an index on a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    index: str
        The index to remove.

    -- Returns
    tuple
        The SQL query to remove the index and the parameters.
    """
    index_query = f"""
    DROP INDEX IF EXISTS idx_{config_definition_key}_{index.replace('.', '_')};
    """

    return index_query, ()


def l_index_query(config_definition_key: str) -> tuple:
    """
    List all indexes on a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    tuple
        The SQL query to list all indexes and the parameters.
    """
    list_query = """
    SELECT indexname
    FROM pg_indexes
    WHERE tablename = %s;
    """

    return list_query, (config_definition_key,)


def c_config_definition_query(config_definition_key: str) -> tuple:
    """
    Create a new configuration definition in the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    tuple
        The SQL query to create the configuration definition and the parameters.
    """
    creation_query = f"""
    CREATE TABLE IF NOT EXISTS {config_definition_key} (
        config_key VARCHAR(255) PRIMARY KEY NOT NULL,
        data JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    return creation_query, ()


def r_config_definition_query(config_definition_key: str) -> tuple:
    """
    Get a configuration definition from the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    tuple
        The SQL query to get the configuration definition and the parameters.
    """
    get_query = f"""
    SELECT * FROM {settings.INTERNAL_TABLE}
    WHERE config_definition_key = %s;
    """
    return get_query, (config_definition_key,)


def d_config_definition_query(config_definition_key: str) -> tuple:
    """
    Delete a configuration table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    tuple
        The SQL query to delete the configuration table and the parameters.
    """
    delete_query = f"""
    DROP TABLE IF EXISTS {config_definition_key};
    """

    return delete_query, ()


def l_config_definition_query(page: int = 1, page_size: int = 10) -> tuple:
    """
    List all configuration definitions.

    -- Parameters
    page: int, optional
        The page number. Defaults to 1.
    page_size: int, optional
        The number of items per page. Defaults to 10.

    -- Returns
    tuple
        The SQL query to list all configuration definitions and the parameters.
    """

    list_query = f"""
    SELECT * FROM {settings.INTERNAL_TABLE}
    LIMIT %s OFFSET %s;
    """

    offset = page_size * (page - 1)
    return list_query, (page_size, offset)
