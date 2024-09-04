"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any


class CreateConfig(BaseModel):
    """
    Represents the configuration for a configuration definition.
    """

    config_key: str = Field(..., description="The unique identifier for the config.")
    data: Dict[str, Any] = Field(..., description="The data for the configuration.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "config_key": "qreate",
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
