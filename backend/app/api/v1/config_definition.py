"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, status

from app.utils.config_definitions.utils import (
    c_config_definition,
    r_config_definition,
    u_config_definition,
    d_config_definition,
    l_config_definition,
)

from app.models.config_definition import (
    ConfigDefinition,
    ConfigDefinitionEditable,
    CreateConfigDefinitionResponse,
    ReadConfigDefinitionResponse,
    UpdateConfigDefinitionResponse,
    DeleteConfigDefinitionResponse,
    ListConfigDefinitionResponse,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateConfigDefinitionResponse,
    response_model_exclude_none=True,
)
def create_config_definition(config_definition: ConfigDefinition):
    """
    Create a new configuration definition.

    -- Parameters
    config_definition: CreateConfigDefinition
        The configuration definition to create.

    -- Returns
    CreateConfigDefinitionResponse
        The response for the create configuration definition request.
    """
    c_config_definition(
        config_definition.config_definition_key,
        config_definition.json_schema,
        config_definition.indexes,
    )

    return {
        "message": "Configuration definition created successfully.",
        "data": config_definition.model_dump(),
    }


@router.get(
    "/{config_definition_key}",
    status_code=status.HTTP_200_OK,
    response_model=ReadConfigDefinitionResponse,
    response_model_exclude_none=True,
)
def get_config_definition(config_definition_key: str):
    """
    Get a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.

    -- Returns
    ReadConfigDefinitionResponse
        The response for the get configuration definition request.
    """
    config_definition = r_config_definition(config_definition_key)

    return {
        "message": "Configuration definition retrieved successfully.",
        "data": config_definition,
    }


@router.put(
    "/{config_definition_key}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateConfigDefinitionResponse,
    response_model_exclude_none=True,
)
def update_config_definition(
    config_definition_key: str, config_definition: ConfigDefinitionEditable
):
    """
    Update a configuration definition.

    -- Parameters
    config_definition_key: str
        The key for the configuration definition.
    config_definition: UpdateConfigDefinition
        The configuration definition to update.

    -- Returns
    UpdateConfigDefinitionResponse
        The response for the update configuration definition request.
    """
    u_config_definition(config_definition_key, config_definition.indexes)

    return {
        "message": "Configuration definition updated successfully.",
        "data": config_definition.model_dump(),
    }


@router.delete(
    "/{config_definition_key}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteConfigDefinitionResponse,
    response_model_exclude_none=True,
)
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
    d_config_definition(config_definition_key)

    return {
        "message": "Configuration definition deleted successfully.",
        "data": {"config_definition_key": config_definition_key},
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ListConfigDefinitionResponse,
    response_model_exclude_none=True,
)
def list_config_definition(
    page: int = 1,
    limit: int = 10,
    sort_by: str = "modified_at",
    sort_order: str = "desc",
    search: str = None,
):
    """
    List all configuration definitions.

    -- Parameters
    page: int
        The page number.
    limit: int
        The limit for the number of configuration definitions to return.
    sort_by: str
        The field to sort by.
    sort_order: str
        The order to sort by.
    search: str
        The search term.

    -- Returns
    ListConfigDefinitionResponse
        The response for the list configuration definition request.
    """
    config_definitions, count = l_config_definition(
        page, limit, sort_by, sort_order, search
    )

    return {
        "message": "Configuration definitions listed successfully.",
        "data": {
            "results": config_definitions,
            "meta": {"page": page, "limit": limit, "total": count},
        },
    }
