"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to store the configuration values
    """

    DB_NAME: str = "datastore"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"


settings = Settings()