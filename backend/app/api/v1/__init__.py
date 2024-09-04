"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import APIRouter, Depends
from app.api.v1.config_definition import router as config_definition_router
from app.api.v1.config import router as config_router
from app.utils.auth.middlewares import check_api_key

api_router = APIRouter()

api_router.include_router(
    config_definition_router,
    prefix="/config_definition",
    tags=["Config Definition"],
    dependencies=[Depends(check_api_key)],
)
api_router.include_router(
    config_router,
    prefix="/config_definition/{config_definition_key}/config",
    tags=["Config"],
    dependencies=[Depends(check_api_key)],
)
