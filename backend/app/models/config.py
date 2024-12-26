"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any
from datetime import datetime

from app.models.common import (
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
    ListResponse,
)


class ConfigEditable(BaseModel):
    """
    Represents the mutable fields for a configuration.
    """

    data: Dict[str, Any] = Field(..., description="The data for the configuration.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": {
                    "setting_string": "value",
                    "setting_object": {
                        "first_key": "value",
                        "second_key": 1,
                    },
                },
            },
        }
    )


class Config(ConfigEditable):
    """
    Represents the configuration.
    """

    config_key: str = Field(..., description="The unique identifier for the config.")


class ConfigIdentity(BaseModel):
    """
    Represents the identity for a configuration.
    """

    config_definition_key: str = Field(
        ..., description="The unique identifier for the config definition."
    )
    config_key: str = Field(..., description="The unique identifier for the config.")


class ConfigRetrievable(Config):
    """
    Represents the configuration with the key.
    """

    created_at: datetime = Field(
        ..., description="The time the configuration was created."
    )
    modified_at: datetime = Field(
        ..., description="The time the configuration was last updated."
    )


class CreateConfigResponse(CreateResponse[Dict[str, Any]]):
    """
    Represents the response for creating a configuration.
    """

    pass


class ReadConfigResponse(ReadResponse[ConfigRetrievable]):
    """
    Represents the response for getting a configuration.
    """

    pass


class UpdateConfigResponse(UpdateResponse[Dict[str, Any]]):
    """
    Represents the response for updating a configuration.
    """

    pass


class DeleteConfigResponse(DeleteResponse[ConfigIdentity]):
    """
    Represents the response for deleting a configuration.
    """

    pass


class ListConfigResponse(ListResponse[ConfigRetrievable]):
    """
    Represents the response for listing configurations.
    """

    pass
