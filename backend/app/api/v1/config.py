"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, HTTPException, Request

from app.utils.configs.utils import c_config, r_config, d_config, l_config, u_config

from app.models.config import CreateConfig, UpdateConfig

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/")
def create_config(config_definition_key: str, config: CreateConfig):
    """
    Create a new configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config: CreateConfig
        The data for the configuration

    -- Returns
    CreateConfigResponse
        The response for the create configuration request.
    """
    try:
        c_config(
            config_definition_key,
            config.config_key,
            config.data,
        )
    except Exception as e:
        logger.exception(f"Error creating configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Configuration created successfully."}


@router.get("/{config_key}")
def get_config(config_definition_key: str, config_key: str):
    """
    Get a configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration

    -- Returns
    ReadConfigResponse
        The response for the get configuration request.
    """
    try:
        config = r_config(
            config_definition_key,
            config_key,
        )
    except Exception as e:
        logger.exception(f"Error reading configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Configuration retrieved successfully.",
        "data": config,
    }


@router.put("/{config_key}")
def update_config(config_definition_key: str, config_key: str, config: UpdateConfig):
    """
    Update an existing configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration to be updated.
    config: UpdateConfig
        The updated data for the configuration.

    -- Returns
    dict
        A success message.
    """
    try:
        u_config(
            config_definition_key,
            config_key,
            config.data,
        )
    except ValueError as e:
        logger.warning(f"Configuration not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Error updating configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Configuration updated successfully."}


@router.delete("/{config_key}")
def delete_config(config_definition_key: str, config_key: str):
    """
    Delete a configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_key: str
        The key for the configuration

    -- Returns
    DeleteConfigResponse
        The response for the delete configuration request.
    """
    try:
        d_config(
            config_definition_key,
            config_key,
        )
    except Exception as e:
        logger.exception(f"Error deleting configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Configuration deleted successfully."}


@router.get("/")
def list_configs(
    request: Request,
    config_definition_key: str,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "modified_at",
    sort_order: str = "desc",
    search: str = None,
):
    """
    List all configurations for a configuration definition.

    -- Parameters
    request: Request
        The request object.
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
        The search term.

    -- Returns
    ListConfigsResponse
        The response for the list configurations request.
    """
    try:
        configs, count = l_config(
            config_definition_key,
            page,
            limit,
            sort_by,
            sort_order,
            search,
            request,
        )

    except Exception as e:
        logger.exception(f"Error listing configurations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Configurations listed successfully.",
        "data": {
            "results": configs,
            "meta": {"page": page, "limit": limit, "total": count},
        },
    }
