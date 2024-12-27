"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.models.common import (
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
    ListResponse,
)


class ConfigDefinitionEditable(BaseModel):
    """
    Represents an existing configuration definition to be updated in the internal table.
    """

    indexes: List[str] = Field(
        default_factory=list,
        description="List of field names to be indexed. Each must exist in the schema properties.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "indexes": ["setting_object.first_key"],
            }
        }
    )


class ConfigDefinition(ConfigDefinitionEditable):
    """
    Represents a new configuration definition to be created in the internal table.
    """

    config_definition_key: str = Field(
        ..., description="The unique identifier for the config definition."
    )
    json_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON Schema for validating configs belonging to this config definition.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "config_definition_key": "app_config",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "setting_string": {"type": "string"},
                        "setting_object": {
                            "type": "object",
                            "properties": {
                                "first_key": {"type": "string"},
                                "second_key": {"type": "integer"},
                            },
                        },
                    },
                    "required": ["setting_string", "setting_object"],
                },
                **ConfigDefinitionEditable.model_config["json_schema_extra"]["example"],
            }
        }
    )


class ConfigDefinitionIdentity(BaseModel):
    """
    Represents the identity for a configuration definition.
    """

    config_definition_key: str = Field(
        ..., description="The unique identifier for the config definition."
    )


class ConfigDefinitionRetrievable(ConfigDefinition):
    """
    Represents the configuration definition with the key.
    """

    created_at: datetime = Field(
        ..., description="The time the configuration definition was created."
    )
    modified_at: datetime = Field(
        ..., description="The time the configuration definition was last updated."
    )


class CreateConfigDefinitionResponse(CreateResponse[ConfigDefinition]):
    """
    Represents the response for the create configuration definition request.
    """

    pass


class ReadConfigDefinitionResponse(ReadResponse[ConfigDefinitionRetrievable]):
    """
    Represents the response for getting a configuration definition.
    """

    pass


class UpdateConfigDefinitionResponse(UpdateResponse[ConfigDefinitionEditable]):
    """
    Represents the response for updating a configuration definition.
    """

    pass


class DeleteConfigDefinitionResponse(DeleteResponse[ConfigDefinitionIdentity]):
    """
    Represents the response for deleting a configuration definition.
    """

    pass


class ListConfigDefinitionResponse(ListResponse[ConfigDefinitionRetrievable]):
    """
    Represents the response for listing configuration definitions.
    """

    pass
