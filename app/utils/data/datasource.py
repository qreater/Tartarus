"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from psycopg2 import connect
from app.utils.config.conf import settings
from app.utils.config.queries import (
    QUERY_CREATE_TABLE,
    QUERY_CREATE_INDEX,
)
import logging

logger = logging.getLogger(__name__)


class DataStore:
    def __init__(self):
        self.connection = None
        self._create_connection()
        self._initialize_table()

    def __del__(self):
        self._close_connection()

    def _execute_query(self, query):
        """
        Execute a SQL query using a cursor, with error handling and cleanup.
        """
        if not self.connection:
            raise RuntimeError("No database connection defined!")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            logger.exception(f"Query execution failed: {e}")

    def _create_internal_table(self):
        """
        Create the internal table to store the configuration
        """
        query = QUERY_CREATE_TABLE
        self._execute_query(query)

    def _create_internal_indexes(self):
        """
        Create the indexes on the internal table
        """
        query = QUERY_CREATE_INDEX
        self._execute_query(query)

    def _create_connection(self):
        """
        Create a connection to the database
        """

        try:
            self.connection = connect(
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )
            self.connection.autocommit = True
            logger.info("DataStore Connection Established!")
        except Exception as e:
            logger.exception(f"DataStore set-up failed: {e}")

    def _initialize_table(self):
        """
        Initialize the table and its indices.
        """
        self._create_internal_table()
        self._create_internal_indexes()

    def _close_connection(self):
        """
        Close the connection to the database
        """
        if self.connection:
            self.connection.close()
            logger.info("DataStore Connection Closed!")


if __name__ == "__main__":
    data_store = DataStore()
