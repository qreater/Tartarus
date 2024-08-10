"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest
from app.utils.data.datasource import DataStore
from app.utils.config.conf import settings


class TestDataStoreIntegration:
    """
    Integration test suite for the DataStore class.
    """

    @pytest.fixture(scope="class")
    def datastore(self):
        """
        Fixture to initialize the DataStore instance for integration tests.
        Ensures that the connection is properly established before tests and
        cleaned up after all tests in the class have run.
        """
        ds = DataStore()
        yield ds
        del ds

    def test_connection_established(self, datastore):
        """
        Test that the DataStore connection is successfully established.

        This test verifies that a connection is established and that it is
        not None, indicating that the database connection is functional.
        """
        assert datastore.connection is not None

    def test_create_database(self, datastore):
        """
        Test that the database is created if it does not exist.

        This test verifies that the DataStore class creates the database
        if it is not already present. It checks for the existence of the
        database by querying the PostgreSQL catalog.
        """
        cursor = datastore.connection.cursor()
        cursor.execute(
            f"SELECT * FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}' LIMIT 1;"
        )
        exists = cursor.fetchone()
        assert exists is not None
