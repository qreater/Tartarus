"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import json
import datetime


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
    data,
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


def l_clause_query(filters: dict, search: str = None) -> tuple:
    """
    Build the WHERE clause and parameter list for SQL queries.

    -- Parameters
    filters: dict
        The filters for the query.
    search: str, optional
        The search term. Defaults to None.

    -- Returns
    tuple
        A tuple containing the WHERE clause string and the parameters.
    """

    filter_clause = (
        " AND ".join(f"{key} = %s" for key in filters) if filters else "1 = 1"
    )
    search_clause = "AND config_key ILIKE %s" if search else ""

    where_clause = f"WHERE {filter_clause} {search_clause}".strip()
    where_clause = where_clause if where_clause != "WHERE" else ""

    params = (*filters.values(), f"%{search}%") if search else (*filters.values(),)
    return where_clause, params


def l_config_query(
    config_definition_key: str,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "modified_at",
    sort_order: str = "desc",
    clause_query: str = "",
    clause_params: tuple = (),
) -> tuple:
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
    clause_query: str, optional
        The WHERE clause for the query. Defaults to "".
    clause_params: tuple, optional
        The parameters for the WHERE clause. Defaults to ().

    -- Returns
    tuple
        The SQL query to list the configurations and the parameters.
    """
    offset = limit * (page - 1)

    query = f"""
    SELECT 
        config_key,
        data,
        created_at,
        modified_at
    FROM {config_definition_key}
    {clause_query}
    ORDER BY {sort_by} {sort_order}
    LIMIT %s OFFSET %s;
    """

    return query, (*clause_params, limit, offset)


def l_config_count_query(
    config_definition_key: str, clause_query: str = "", clause_params: tuple = ()
) -> tuple:
    """
    Get the total number of configuration definitions for the query.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    clause_query: str
        The WHERE clause for the query. Defaults to "".
    clause_params: tuple
        The parameters for the WHERE clause. Defaults to ().

    -- Returns
    tuple
        The SQL query to get the total count and the parameters.
    """

    count_query = f"""
    SELECT COUNT(*) FROM {config_definition_key} {clause_query};
    """

    return count_query, clause_params
