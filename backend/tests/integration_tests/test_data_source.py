"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest
from app.utils.data.data_source import DataStore
from app.utils.settings.config import settings


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

    def test_create_internal_table(self, datastore):
        """
        Test that the internal table is created in the database.

        This test verifies that the internal table is created by checking
        the PostgreSQL catalog for the presence of the table.
        """
        cursor = datastore.connection.cursor()
        cursor.execute(
            f"SELECT * FROM pg_catalog.pg_tables WHERE tablename = '{settings.INTERNAL_TABLE}' LIMIT 1;"
        )
        exists = cursor.fetchone()
        assert exists is not None
        cursor.close()

    def test_create_internal_indexes(self, datastore):
        """
        Test that the indexes are created on the internal table.

        This test verifies that the indexes on the internal table are created
        by checking the PostgreSQL catalog for the presence of the indexes.
        """
        cursor = datastore.connection.cursor()
        cursor.execute(
            f"SELECT * FROM pg_indexes WHERE tablename = '{settings.INTERNAL_TABLE}';"
        )
        indexes = cursor.fetchall()
        assert len(indexes) == 3
        cursor.close()
