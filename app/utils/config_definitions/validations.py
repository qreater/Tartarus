"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import jsonschema
from typing import Any, Dict, List


def validate_schema_structure(json_schema: Dict[str, Any]) -> None:
    """
    Validates the structure of the provided JSON Schema, ensuring it is correct and well-formed.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to be validated.

    """
    try:
        if not json_schema:
            return
        jsonschema.Draft7Validator.check_schema(json_schema)
    except jsonschema.exceptions.SchemaError as e:
        raise ValueError(f"Invalid JSON Schema provided: {e.message}")


def validate_schema_index(json_schema: Dict[str, Any], indexes: List[str]) -> None:
    """
    Ensures that each secondary index field exists in the schema properties.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.
    indexes: List[str]
        The index fields to validate.

    """
    if not json_schema:
        return

    for index in indexes:
        if not validate_schema_property(index, json_schema):
            raise ValueError(
                f"The index '{index}' is not defined in the schema properties."
            )


def validate_index(indexes: List[str]) -> None:
    """
    Validates the secondary index fields.

    -- Parameters
    indexes: List[str]
        The secondary index fields to validate.

    """
    if len(indexes) != len(set(indexes)):
        raise ValueError("Duplicate secondary indexes are not allowed.")


def validate_schema_property(field_path: str, json_schema: Dict[str, Any]) -> bool:
    """
    Helper method to verify that a nested field path exists in the schema properties.
    Supports nested paths via dot notation.

    -- Parameters
    field_path: str
        The field path to validate.
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.

    -- Returns
    bool
        True if the field path exists in the schema properties, False otherwise

    """
    properties = json_schema.get("properties", {})
    keys = field_path.split(".")
    for key in keys:
        if key in properties:
            properties = properties[key].get("properties", {})
        else:
            return False

    return True


def validate_config_creation(json_schema: Dict[str, Any], indexes: List[str]) -> None:
    """
    Validates the creation of a new configuration definition.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.
    indexes: List[str]
        The secondary index fields to validate.

    """
    validate_index(indexes)

    validate_schema_structure(json_schema)
    validate_schema_index(json_schema, indexes)
    return None


def validate_config_update(json_schema: Dict[str, Any], indexes: List[str]) -> None:
    """
    Validates the update of an existing configuration definition.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.
    indexes: List[str]
        The index fields to validate.

    """
    validate_index(indexes)

    validate_schema_structure(json_schema)
    validate_schema_index(json_schema, indexes)


def validate_list_params(page: int, page_size: int) -> None:
    """
    Validates the parameters for listing configuration definitions.

    -- Parameters
    page_number: int
        The page number to validate.
    items_per_page: int
        The items per page to validate.

    """
    if page < 1 or page_size < 1:
        raise ValueError("Page number and page size must be greater than 0.")
    if page_size > 100:
        raise ValueError("Page size must not exceed 100.")
