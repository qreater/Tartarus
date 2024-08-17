"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import FastAPI
import logging

from app.utils.data.data_source import DataStore

app = FastAPI()
data_store = DataStore()

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

from app.api.v1 import api_router as api_router_v1

app.include_router(api_router_v1, prefix="/api/v1")


@app.get("/")
@app.get("/health")
@app.get("/readiness-probe")
def health_check():
    """
    Health check, Welcomes a user to the API
    """
    return {"message": "Welcome to Tartarus API"}
