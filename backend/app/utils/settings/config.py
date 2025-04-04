"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to store the configuration values

    -- Parameters
    API_KEY: str
        The API key to access the API.
    DB_NAME: str
        The name of the database.
    DB_USER: str
        The database user.
    DB_PASSWORD: str
        The database password.
    DB_HOST: str
        The database host.
    DB_PORT: str
        The database port.
    INTERNAL_TABLE: str
        The internal table name.
    """

    API_KEY: str = "OPEN_SESAME"

    DB_NAME: str = "datastore"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"

    INTERNAL_TABLE: str = "tartarus_internal_cft"


settings = Settings()
