"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock
from app.utils.config.conf import settings
from app.utils.config.queries import (
    QUERY_CREATE_TABLE,
    QUERY_CREATE_INDEX,
)
from app.utils.data.data_source import DataStore


class TestDataStore:
    """
    Test suite for the DataStore class.
    """

    @patch("app.utils.data.data_source.connect")
    def test_does_create_connection(self, mock_connect):
        """
        Test that the DataStore class correctly establishes a database connection.

        This test mocks the `connect` function from psycopg2 to simulate
        the creation of a database connection. It verifies that the connection
        is established with the correct parameters and that autocommit is enabled.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        ds = DataStore()

        mock_connect.assert_called_once_with(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
        )
        assert ds.connection == mock_conn
        assert ds.connection.autocommit is True
        del ds

    @patch("app.utils.data.data_source.connect")
    def test_does_create_internal_table(self, mock_connect):
        """
        Test that the DataStore class correctly creates the internal table.

        This test mocks the `connect` function and verifies that the internal
        table is created with the correct schema.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        ds = DataStore()

        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.assert_any_call(QUERY_CREATE_TABLE)
        del ds

    @patch("app.utils.data.data_source.connect")
    def test_does_create_internal_indexes(self, mock_connect):
        """
        Test that the DataStore class correctly creates the indexes on the internal table.

        This test mocks the `connect` function and verifies that the indexes
        are created on the internal table.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        ds = DataStore()

        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.assert_any_call(QUERY_CREATE_INDEX)
        del ds

    @patch("app.utils.data.data_source.connect")
    def test_does_close_connection(self, mock_connect):
        """
        Test that the DataStore class correctly closes the database connection.

        This test mocks the `connect` function and verifies that the connection
        is closed when the DataStore instance is deleted.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        ds = DataStore()
        del ds

        mock_conn.close.assert_called_once()
