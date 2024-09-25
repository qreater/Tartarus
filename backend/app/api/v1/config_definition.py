"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, HTTPException

from app.utils.config_definitions.utils import (
    c_config_definition,
    r_config_definition,
    u_config_definition,
    d_config_definition,
    l_config_definition,
)

from app.models.config_definition import CreateConfigDefinition, UpdateConfigDefinition

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/")
def create_config_definition(config_definition: CreateConfigDefinition):
    """
    Create a new configuration definition.

    -- Parameters
    config_definition: CreateConfigDefinition
        The configuration definition to create.

    -- Returns
    CreateConfigDefinitionResponse
        The response for the create configuration definition request.
    """
    try:
        c_config_definition(
            config_definition.config_definition_key,
            config_definition.json_schema,
            config_definition.indexes,
        )
    except Exception as e:
        logger.exception(f"Error creating configuration definition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Configuration definition created successfully."}


@router.get("/{config_definition_key}")
def get_config_definition(config_definition_key: str):
    """
    Get a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    GetConfigDefinitionResponse
        The response for the get configuration definition request.
    """
    try:
        config_definition = r_config_definition(config_definition_key)
    except Exception as e:
        logger.exception(f"Error retrieving configuration definition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Configuration definition retrieved successfully.",
        "data": config_definition,
    }


@router.put("/{config_definition_key}")
def update_config_definition(
    config_definition_key: str, config_definition: UpdateConfigDefinition
):
    """
    Update a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_definition: UpdateConfigDefinition
        The configuration definition to update.

    -- Returns
    CreateConfigDefinitionResponse
        The response for the update configuration definition request.
    """
    try:
        u_config_definition(config_definition_key, config_definition.indexes)
    except Exception as e:
        logger.exception(f"Error updating configuration definition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Configuration definition updated successfully."}


@router.delete("/{config_definition_key}")
def delete_config_definition(config_definition_key: str):
    """
    Delete a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    DeleteConfigDefinitionResponse
        The response for the delete configuration definition request.
    """
    try:
        d_config_definition(config_definition_key)

    except Exception as e:
        logger.exception(f"Error deleting configuration definition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Configuration definition deleted successfully."}


@router.get("/")
def list_config_definition(page: int = 1, limit: int = 10):
    """
    List all configuration definitions.

    -- Returns
    ListConfigDefinitionResponse
        The response for the list configuration definition request.
    """
    try:
        config_definitions = l_config_definition(page, limit)

    except Exception as e:
        logger.exception(f"Error listing configuration definitions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Configuration definitions listed successfully.",
        "data": config_definitions,
    }
