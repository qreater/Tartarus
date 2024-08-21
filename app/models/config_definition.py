"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List


class CreateConfigDefinition(BaseModel):
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
    primary_key: str = Field(
        ...,
        description="Field name to be used as the primary key. Must exist in the schema properties.",
    )
    secondary_indexes: Optional[List[str]] = Field(
        default_factory=list,
        description="List of field names to be indexed. Each must exist in the schema properties.",
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
                "primary_key": "setting_string",
                "secondary_indexes": ["setting_object.first_key"],
            }
        }
    )


class UpdateConfigDefinition(BaseModel):
    """
    Represents an existing configuration definition to be updated in the internal table.
    """

    secondary_indexes: List[str] = Field(
        default_factory=list,
        description="List of field names to be indexed. Each must exist in the schema properties.",
    )
