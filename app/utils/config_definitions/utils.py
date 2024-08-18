"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.config_definitions.queries import (
    internal_c_definition_query,
    internal_u_definition_query,
    internal_d_definition_query,
    c_index_query,
    d_index_query,
    l_index_query,
    c_config_definition_query,
    r_config_definition_query,
    d_config_definition_query,
    l_config_definition_query,
)

from app.utils.config_definitions.validations import (
    validate_config_creation,
    validate_config_update,
)

from app.utils.data.data_source import DataStore

data_store = DataStore()


def c_config_definition(
    config_type_key: str, json_schema: dict, primary_key: str, secondary_indexes: list
):
    """
    Create a new configuration definition in the internal table.

    -- Parameters
    config_type_key: str
        The key for the configuration type.
    json_schema: dict
        The JSON schema for the configuration type.
    primary_key: str
        The primary key for the configuration type.
    secondary_indexes: list
        The secondary indexes for the configuration type.

    -- Returns
    None
    """

    validate_config_creation(json_schema, primary_key, secondary_indexes)

    internal_query = internal_c_definition_query(
        config_type_key, json_schema, primary_key, secondary_indexes
    )
    data_store._execute_query(internal_query)

    creation_query = c_config_definition_query(config_type_key, primary_key)
    data_store._execute_query(creation_query)

    for index in secondary_indexes:
        index_query = c_index_query(config_type_key, index)
        data_store._execute_query(index_query)

    index_query = c_index_query(config_type_key, primary_key)
    data_store._execute_query(index_query)

    return None


def r_config_definition(config_type_key: str):
    """
    Get a configuration definition from the internal table.

    -- Parameters
    config_type_key: str
        The key for the configuration type.

    -- Returns
    dict
        The configuration definition.
    """

    query = r_config_definition_query(config_type_key)
    result = data_store._execute_query(query, mode="retrieve")

    if len(result) == 0 or result is None:
        raise Exception("Configuration definition not found.")

    return result[0]


def u_config_definition(config_type_key: str, secondary_indexes: list):
    """
    Update a configuration definition in the internal table.

    -- Parameters
    config_type_key: str
        The key for the configuration type.
    secondary_indexes: list
        The secondary indexes for the configuration type.

    -- Returns
    None
    """

    config_definition = r_config_definition(config_type_key)
    json_schema = config_definition["json_schema"]

    validate_config_update(json_schema, secondary_indexes)

    internal_query = internal_u_definition_query(config_type_key, secondary_indexes)
    data_store._execute_query(internal_query)

    list_query = l_index_query(config_type_key)

    result = data_store._execute_query(list_query, mode="retrieve")
    existing_indexes = [index["indexname"] for index in result]

    for index in secondary_indexes:
        if index not in existing_indexes:
            index_query = c_index_query(config_type_key, index)
            data_store._execute_query(index_query)

    for index in existing_indexes:
        if index not in secondary_indexes:
            index_query = d_index_query(config_type_key, index)
            data_store._execute_query(index_query)

    return None


def d_config_definition(config_type_key: str):
    """
    Delete a configuration definition from the internal table.

    -- Parameters
    config_type_key: str
        The key for the configuration type.

    -- Returns
    None
    """
    internal_query = internal_d_definition_query(config_type_key)
    data_store._execute_query(internal_query)

    delete_query = d_config_definition_query(config_type_key)
    data_store._execute_query(delete_query)

    return None


def l_config_definition(page: int, page_size: int):
    """
    List configuration definitions from the internal table.

    -- Parameters
    page: int
        The page number.
    page_size: int
        The number of items per page.

    -- Returns
    list
        The configuration definitions.
    """
    query = l_config_definition_query(page, page_size)
    result = data_store._execute_query(query, mode="retrieve")

    return result
