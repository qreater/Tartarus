"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import jsonschema
import re

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
            "Configuration key must start with a letter and contain only alphanumeric characters and underscores."
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
    validate_config_key(config_key)
    validate_config_data(config_definition_key, data)

    return None