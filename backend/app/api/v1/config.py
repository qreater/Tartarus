"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, HTTPException

from app.utils.configs.utils import (
    c_config,
)

from app.models.config import CreateConfig

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/")
def create_config(config_definition_key: str, config: CreateConfig):
    """
    Create a new configuration.

    -- Parameters
    config_definition_key: str
        The key for the configuration type.
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
