"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from psycopg2 import connect
from app.utils.config.conf import settings
import logging

logger = logging.getLogger(__name__)


class DataStore:
    def __init__(self):
        self._create_connection()

    def __del__(self):
        self._close_connection()

    def _create_database(self):
        """
        Create the database if it does not exist
        """

        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT * FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}' LIMIT 1;"
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {settings.DB_NAME}")
            logger.info(f"Database '{settings.DB_NAME}' created successfully!")
        else:
            logger.info(f"Database '{settings.DB_NAME}' already exists!")

    def _create_connection(self):
        """
        Create a connection to the database
        """

        try:
            self.connection = connect(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )
            self.connection.autocommit = True
            logger.info("DataStore Connection Established!")
            self._create_database()
        except Exception as e:
            logger.exception(f"DataStore set-up failed: {e}")

    def _close_connection(self):
        """
        Close the connection to the database
        """
        if self.connection:
            self.connection.close()
            logger.info("DataStore Connection Closed!")


if __name__ == "__main__":
    data_store = DataStore()
