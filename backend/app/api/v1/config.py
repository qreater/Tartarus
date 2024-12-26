"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, Request, status

from app.utils.configs.utils import c_config, r_config, d_config, l_config, u_config

from app.models.config import (
    Config,
    ConfigEditable,
    CreateConfigResponse,
    ReadConfigResponse,
    UpdateConfigResponse,
    DeleteConfigResponse,
    ListConfigResponse,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateConfigResponse,
    response_model_exclude_none=True,
)
def create_config(config_definition_key: str, config: Config):
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
    c_config(
        config_definition_key,
        config.config_key,
        config.data,
    )

    return {
        "message": "Configuration created successfully.",
        "data": config.data,
    }


@router.get(
    "/{config_key}",
    status_code=status.HTTP_200_OK,
    response_model=ReadConfigResponse,
    response_model_exclude_none=True,
)
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
    config = r_config(
        config_definition_key,
        config_key,
    )

    return {
        "message": "Configuration retrieved successfully.",
        "data": config,
    }


@router.put(
    "/{config_key}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateConfigResponse,
    response_model_exclude_none=True,
)
def update_config(config_definition_key: str, config_key: str, config: ConfigEditable):
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
    UpdateConfigResponse
        The response for the update configuration request.
    """
    u_config(
        config_definition_key,
        config_key,
        config.data,
    )

    return {
        "message": "Configuration updated successfully.",
        "data": config.data,
    }


@router.delete(
    "/{config_key}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteConfigResponse,
    response_model_exclude_none=True,
)
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
    d_config(
        config_definition_key,
        config_key,
    )

    return {
        "message": "Configuration deleted successfully.",
        "data": {
            "config_definition_key": config_definition_key,
            "config_key": config_key,
        },
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ListConfigResponse,
    response_model_exclude_none=True,
)
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
    ListConfigResponse
        The response for the list configurations request.
    """
    configs, count = l_config(
        config_definition_key,
        page,
        limit,
        sort_by,
        sort_order,
        search,
        request,
    )

    return {
        "message": "Configurations listed successfully.",
        "data": {
            "results": configs,
            "meta": {"page": page, "limit": limit, "total": count},
        },
    }
