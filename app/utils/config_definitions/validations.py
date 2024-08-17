import jsonschema
from typing import Any, Dict, List


def validate_schema_structure(json_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates the structure of the provided JSON Schema, ensuring it is correct and well-formed.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to be validated.

    -- Returns
    Dict[str, Any]
        The validated JSON Schema.
    """
    try:
        jsonschema.Draft7Validator.check_schema(json_schema)
    except jsonschema.exceptions.SchemaError as e:
        raise ValueError(f"Invalid JSON Schema provided: {e.message}")
    return json_schema


def validate_primary_key_exists(json_schema: Dict[str, Any], primary_key: str) -> str:
    """
    Ensures that the primary key field exists in the schema properties.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.

    primary_key: str
        The primary key field to validate.

    -- Returns
    str
        The validated primary key field.

    """

    if json_schema and not is_valid_schema_property(primary_key, json_schema):
        raise ValueError(
            f"The primary key '{primary_key}' is not defined in the schema properties."
        )
    return primary_key


def validate_secondary_indexes_exist(
    json_schema: Dict[str, Any], secondary_indexes: List[str]
) -> List[str]:
    """
    Ensures that each secondary index field exists in the schema properties.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.
    secondary_indexes: List[str]
        The secondary index fields to validate.

    -- Returns
    List[str]
        The validated secondary index fields

    """
    for index in secondary_indexes:
        print(index)
        if not is_valid_schema_property(index, json_schema):
            raise ValueError(
                f"The secondary index '{index}' is not defined in the schema properties."
            )
    return secondary_indexes


def is_valid_schema_property(field_path: str, json_schema: Dict[str, Any]) -> bool:
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


def validate_config_creation(
    json_schema: Dict[str, Any], primary_key: str, secondary_indexes: List[str]
) -> None:
    """
    Validates the creation of a new configuration definition.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.
    primary_key: str
        The primary key field to validate.
    secondary_indexes: List[str]
        The secondary index fields to validate.

    -- Returns
    None
    """
    validate_schema_structure(json_schema)
    validate_primary_key_exists(json_schema, primary_key)
    validate_secondary_indexes_exist(json_schema, secondary_indexes)
    return None


def validate_config_update(
    json_schema: Dict[str, Any], secondary_indexes: List[str]
) -> None:
    """
    Validates the update of an existing configuration definition.

    -- Parameters
    json_schema: Dict[str, Any]
        The JSON Schema to validate against.
    secondary_indexes: List[str]
        The secondary index fields to validate.

    -- Returns
    None
    """
    validate_schema_structure(json_schema)
    validate_secondary_indexes_exist(json_schema, secondary_indexes)
    return None
