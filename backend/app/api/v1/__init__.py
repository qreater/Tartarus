"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter
from app.api.v1.config_definition import router as config_definition_router

api_router = APIRouter()
api_router.include_router(
    config_definition_router, prefix="/config_definition", tags=["Config Definition"]
)