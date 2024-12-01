"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import jsonschema
import re
from fastapi import Request

from app.utils.config_definitions.validations import (
    validate_config_definition_key,
    validate_list_params,
)
from app.utils.config_definitions.utils import r_config_definition


def validate_config_key(config_key: str) -> None:
    """
    Validates the configuration key.

    -- Parameters
    config_key: str
        The configuration key to validate.

    """
    if not config_key:
        raise ValueError("Configuration key must be provided.")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{2,}$", config_key):
        raise ValueError(
            "Configuration key must start with a letter and contain only alphanumeric characters and underscores and be at least 3 characters long."
        )


def validate_config_data(config_definition_key: str, data: dict) -> None:
    """
    Validates the configuration data.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    data: dict
        The data for the configuration
    """
    if not data:
        raise ValueError("Configuration data must be provided.")

    config_definition = r_config_definition(config_definition_key)
    json_schema = config_definition.get("json_schema")

    if not json_schema:
        return

    try:
        jsonschema.validate(data, json_schema)
    except jsonschema.ValidationError as e:
        raise ValueError(f"Configuration schema mismatch: {e.message}")


def validate_config_creation(
    config_definition_key: str, config_key: str, data: dict
) -> None:
    """
    Validates the creation of a new configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.
    data: dict
        The data for the configuration.
    """
    validate_config_definition_key(config_definition_key)
    validate_config_key(config_key)
    validate_config_data(config_definition_key, data)

    return None


def validate_config_read(config_definition_key: str, config_key: str) -> None:
    """
    Validates the retrieval of a configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.
    """
    r_config_definition(config_definition_key)
    validate_config_key(config_key)

    return None


def validate_config_update(
    config_definition_key: str, config_key: str, data: dict
) -> None:
    """
    Validates the update of an existing configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration to be updated.
    data: dict
        The updated data for the configuration.
    """
    validate_config_definition_key(config_definition_key)
    validate_config_key(config_key)
    validate_config_data(config_definition_key, data)

    return None


def validate_config_deletion(config_definition_key: str, config_key: str) -> None:
    """
    Validates the deletion of a configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration.
    """
    r_config_definition(config_definition_key)
    validate_config_key(config_key)

    return None


def validate_config_list(
    config_definition_key: str,
    page: int,
    limit: int,
    sort_by: str,
    sort_order: str,
    search: str,
    request: Request,
) -> None:
    """
    Validates the listing of configurations.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    page: int
        The page number.
    limit: int
        The number of configurations to list per page.
    sort_by: str
        The field to sort by.
    sort_order: str
        The order to sort by.
    search: str
        The search term to validate.
    request: Request
        The request object.
    """
    config_definition = r_config_definition(config_definition_key)
    indexes = config_definition.get("indexes", [])

    sortable_fields = {"config_key", "created_at", "modified_at", *indexes}
    query_fields = {"page", "limit", "sort_by", "sort_order", "search"}

    filterable_fields = {
        field
        for field in {*indexes, *sortable_fields, *query_fields}
        if field != "config_key"
    }

    for key in request.query_params.keys():
        if key not in filterable_fields:
            raise ValueError(
                f"Invalid filter field: Filter keys must be one of the indexes, or 'created_at', 'modified_at'."
            )

    validate_list_params(sortable_fields, page, limit, sort_by, sort_order, search)

    return None
