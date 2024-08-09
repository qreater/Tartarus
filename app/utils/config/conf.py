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
