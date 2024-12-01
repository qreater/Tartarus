"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import Request

from app.utils.configs.queries import (
    c_config_query,
    r_config_query,
    d_config_query,
    l_clause_query,
    l_config_query,
    l_config_count_query,
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


def l_c_json_path(keys: list[str]) -> str:
    """
    Constructs a JSON path for a given list of keys.

    -- Parameters
    keys: list[str]
        The list of keys representing the path in a JSON object.

    -- Returns
    str
        The JSON path string.
    """
    if len(keys) == 1:
        return f"data->>'{keys[0]}'"
    return "data->" + "->".join([f"'{key}'" for key in keys[:-1]]) + f"->>'{keys[-1]}'"


def l_c_sort_field(sort_by: str, allowed_fields: set[str]) -> str:
    """
    Validates and constructs the sort field.

    -- Parameters
    sort_by: str
        The field to sort by.
    allowed_fields: set[str]
        A set of allowed top-level sort fields.

    -- Returns
    str
        The validated or constructed sort field.
    """
    if sort_by in allowed_fields:
        return sort_by

    keys = sort_by.split(".")
    return l_c_json_path(keys)


def l_util_filters(request: Request) -> dict:
    """
    Extracts the filters from the request query parameters.

    -- Parameters
    request: Request
        The request object.

    -- Returns
    dict
        The filters for the configuration.
    """
    request_filters = request.query_params.items()
    query_fields = {"page", "limit", "sort_by", "sort_order", "search"}

    filters = {}
    for key, value in request_filters:
        if key in query_fields:
            continue

        keys = key.split(".")
        json_path = l_c_json_path(keys)
        filters[json_path] = value

    return filters


def l_util_sort(sort_by: str) -> str:
    """
    Extracts the sort field from the request query parameters.

    -- Parameters
    sort_by: str
        The field to sort by.

    -- Returns
    str
        The field to sort by.
    """
    sortable_fields = {"config_key", "created_at", "modified_at"}
    return l_c_sort_field(sort_by, sortable_fields)


def l_config(
    config_definition_key: str,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "modified_at",
    sort_order: str = "desc",
    search: str = None,
    request: Request = None,
):
    """
    List all configurations for a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    page: int, optional
        The page number. Defaults to 1.
    limit: int, optional
        The number of configurations to list per page. Defaults to 10.
    sort_by: str, optional
        The field to sort by. Defaults to "modified_at".
    sort_order: str, optional
        The sort order. Defaults to "desc".
    search: str, optional
        The search term. Defaults to None.
    request: Request, optional
        The request object. Defaults to None

    -- Returns
    tuple
        The configurations and the count of configurations.
    """
    validate_config_list(
        config_definition_key, page, limit, sort_by, sort_order, search, request
    )

    filters = l_util_filters(request)
    sort_by = l_util_sort(sort_by)

    clause_query, clause_params = l_clause_query(filters, search)

    query, params = l_config_query(
        config_definition_key,
        page,
        limit,
        sort_by,
        sort_order,
        clause_query,
        clause_params,
    )
    result = data_store.execute_query(query, params=params, mode="retrieve")["response"]

    count_query, count_params = l_config_count_query(
        config_definition_key, clause_query, clause_params
    )
    count_result = data_store.execute_query(count_query, count_params, mode="retrieve")[
        "response"
    ]
    count_result = count_result[0]["count"]

    return result, count_result
