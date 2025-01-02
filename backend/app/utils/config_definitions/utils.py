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
    l_config_definition_count_query,
)

from app.utils.config_definitions.validations import (
    validate_config_creation,
    validate_config_read,
    validate_config_update,
    validate_config_delete,
    validate_list_params,
)

from app.utils.exceptions.errors import (
    not_found_error,
)

from app.utils.data.data_source import DataStore

data_store = DataStore()


def c_config_definition(config_definition_key: str, json_schema: dict, indexes: list):
    """
    Create a new configuration definition in the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    json_schema: dict
        The JSON schema for the configuration definition.
    indexes: list
        The indexes for the configuration definition.

    """

    validate_config_creation(config_definition_key, json_schema, indexes)

    internal_query, internal_params = internal_c_definition_query(
        config_definition_key, json_schema, indexes
    )
    data_store.execute_query(internal_query, internal_params)

    creation_query, creation_params = c_config_definition_query(config_definition_key)
    data_store.execute_query(creation_query, creation_params)

    for index in indexes:
        index_query, index_params = c_index_query(config_definition_key, index)
        data_store.execute_query(index_query, index_params)

    return None


def r_config_definition(config_definition_key: str):
    """
    Get a configuration definition from the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    dict
        The configuration definition.
    """
    validate_config_read(config_definition_key)
    query, params = r_config_definition_query(config_definition_key)
    result = data_store.execute_query(query, params=params, mode="retrieve")["response"]

    if len(result) == 0 or result is None:
        raise not_found_error("definition", config_definition_key)

    return result[0]


def u_config_definition(config_definition_key: str, indexes: list):
    """
    Update a configuration definition in the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    indexes: list
        The indexes for the configuration definition.

    """

    config_definition = r_config_definition(config_definition_key)
    json_schema = config_definition["json_schema"]

    validate_config_update(json_schema, indexes)

    internal_query, internal_params = internal_u_definition_query(
        config_definition_key, indexes
    )
    data_store.execute_query(internal_query, internal_params)

    list_query, list_params = l_index_query(config_definition_key)

    result = data_store.execute_query(list_query, params=list_params, mode="retrieve")[
        "response"
    ]
    existing_indexes = [index["indexname"] for index in result]

    for index in indexes:
        if index not in existing_indexes:
            index_query, index_params = c_index_query(config_definition_key, index)
            data_store.execute_query(index_query, index_params)

    for index in existing_indexes:
        if index not in indexes:
            index_query, index_params = d_index_query(config_definition_key, index)
            data_store.execute_query(index_query, index_params)

    return None


def d_config_definition(config_definition_key: str):
    """
    Delete a configuration definition from the internal table.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    None
    """

    validate_config_delete(config_definition_key)

    internal_query, internal_params = internal_d_definition_query(config_definition_key)
    rows_affected = data_store.execute_query(internal_query, internal_params)[
        "rows_affected"
    ]

    if rows_affected == 0:
        raise not_found_error("definition", config_definition_key)

    delete_query, delete_params = d_config_definition_query(config_definition_key)
    data_store.execute_query(delete_query, delete_params)

    return None


def l_config_definition(
    page: int = 1,
    limit: int = 10,
    sort_by: str = "modified_at",
    sort_order: str = "desc",
    search: str = None,
):
    """
    List configuration definitions from the internal table.

    -- Parameters
    page: int, optional
        The page number. Defaults to 1.
    limit: int, optional
        The number of items per page. Defaults to 10.
    sort_by: str, optional
        The field to sort by. Defaults to "modified_at".
    sort_order: str, optional
        The sort order. Defaults to "desc".
    search: str, optional
        The search term. Defaults to None.

    -- Returns
    tuple
        The configuration definitions and the count of configuration
        definitions.
    """
    sortable_fields = {"config_definition_key", "created_at", "modified_at"}
    validate_list_params(sortable_fields, page, limit, sort_by, sort_order, search)

    query, params = l_config_definition_query(page, limit, sort_by, sort_order, search)
    result = data_store.execute_query(query, params=params, mode="retrieve")["response"]

    count_query, count_params = l_config_definition_count_query(search)
    count_result = data_store.execute_query(
        count_query, params=count_params, mode="retrieve"
    )["response"]
    count_result = count_result[0]["count"]

    return result, count_result
