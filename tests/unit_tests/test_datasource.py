"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock
from app.utils.config.conf import settings
from app.utils.data.datasource import DataStore


class TestDataStore:
    """
    Test suite for the DataStore class.
    """

    @patch("app.utils.data.datasource.connect")
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
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
        )
        assert ds.connection == mock_conn
        assert ds.connection.autocommit is True
        del ds

    @patch("app.utils.data.datasource.connect")
    def test_if_create_database_exists(self, mock_connect):
        """
        Test that the DataStore class does not attempt to create a database
        if it already exists.

        This test mocks the `connect` function and simulates the scenario where
        the database already exists. It verifies that the `CREATE DATABASE`
        command is not executed if the database is found.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = True

        ds = DataStore()

        mock_cursor.execute.assert_called_with(
            f"SELECT * FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}' LIMIT 1;"
        )
        assert mock_cursor.fetchone.called
        assert not mock_cursor.execute.call_count == 2
        del ds

    @patch("app.utils.data.datasource.connect")
    def test_if_create_database_not_exists(self, mock_connect):
        """
        Test that the DataStore class creates the database if it does not exist.

        This test mocks the `connect` function and simulates the scenario where
        the database does not exist. It verifies that the `CREATE DATABASE`
        command is executed if the database is not found.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None

        ds = DataStore()

        assert mock_cursor.execute.call_count == 2
        mock_cursor.execute.assert_any_call(
            f"SELECT * FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}' LIMIT 1;"
        )
        mock_cursor.execute.assert_any_call(f"CREATE DATABASE {settings.DB_NAME}")
        del ds

    @patch("app.utils.data.datasource.connect")
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
