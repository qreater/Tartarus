"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import FastAPI
import logging

from app.utils.data.datasource import DataStore

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

data_store = DataStore()


@app.get("/")
@app.get("/health")
@app.get("/readiness-probe")
def health_check():
    """
    Health check, Welcomes a user to the API
    """
    return {"message": "Welcome to Tartarus API"}
