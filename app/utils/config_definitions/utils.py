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
    validate_config_read,
    validate_config_update,
    validate_config_delete,
    validate_list_params,
)

from app.utils.data.data_source import DataStore

data_store = DataStore()


def c_config_definition(config_type_key: str, json_schema: dict, indexes: list):
    """
    Create a new configuration definition in the internal table.

    -- Parameters
    config_type_key: str
        The key for the configuration type.
    json_schema: dict
        The JSON schema for the configuration type.
    indexes: list
        The indexes for the configuration type.

    """

    validate_config_creation(config_type_key, json_schema, indexes)

    internal_query, internal_params = internal_c_definition_query(
        config_type_key, json_schema, indexes
    )
    data_store._execute_query(internal_query, internal_params)

    creation_query, creation_params = c_config_definition_query(config_type_key)
    data_store._execute_query(creation_query, creation_params)

    for index in indexes:
        index_query, index_params = c_index_query(config_type_key, index)
        data_store._execute_query(index_query, index_params)

    index_query, index_params = c_index_query(config_type_key, index)
    data_store._execute_query(index_query, index_params)

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

    validate_config_read(config_type_key)

    query, params = r_config_definition_query(config_type_key)
    result = data_store._execute_query(query, params=params, mode="retrieve")

    if len(result) == 0 or result is None:
        raise ValueError("Configuration definition not found.")

    return result[0]


def u_config_definition(config_type_key: str, indexes: list):
    """
    Update a configuration definition in the internal table.

    -- Parameters
    config_type_key: str
        The key for the configuration type.
    indexes: list
        The indexes for the configuration type.

    """

    config_definition = r_config_definition(config_type_key)
    json_schema = config_definition["json_schema"]

    validate_config_update(json_schema, indexes)

    internal_query, internal_params = internal_u_definition_query(
        config_type_key, indexes
    )
    data_store._execute_query(internal_query, internal_params)

    list_query, list_params = l_index_query(config_type_key)

    result = data_store._execute_query(list_query, params=list_params, mode="retrieve")
    existing_indexes = [index["indexname"] for index in result]

    for index in indexes:
        if index not in existing_indexes:
            index_query, index_params = c_index_query(config_type_key, index)
            data_store._execute_query(index_query, index_params)

    for index in existing_indexes:
        if index not in indexes:
            index_query, index_params = d_index_query(config_type_key, index)
            data_store._execute_query(index_query, index_params)

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

    validate_config_delete(config_type_key)

    internal_query, internal_params = internal_d_definition_query(config_type_key)
    data_store._execute_query(internal_query, internal_params)

    delete_query, delete_params = d_config_definition_query(config_type_key)
    data_store._execute_query(delete_query, delete_params)

    return None


def l_config_definition(page: int = 1, page_size: int = 10):
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

    validate_list_params(page, page_size)

    query, params = l_config_definition_query(page, page_size)
    result = data_store._execute_query(query, params=params, mode="retrieve")

    return result
