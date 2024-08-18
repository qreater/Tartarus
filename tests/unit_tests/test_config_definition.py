"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock

with patch("app.utils.data.data_source.connect") as mock_connect:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    from app.utils.config_definitions.utils import (
        c_config_definition,
        r_config_definition,
        u_config_definition,
        d_config_definition,
        l_config_definition,
    )

from app.utils.config_definitions.queries import (
    internal_c_definition_query,
    internal_u_definition_query,
    internal_d_definition_query,
    c_index_query,
    d_index_query,
    l_index_query,
    c_config_definition_query,
    r_config_definition_query,
    d_config_definition_query,
    l_config_definition_query,
)

from app.utils.data.data_source import DataStore


class TestConfigDefinitionUnit:
    """
    Test suite for the config definition utility functions.
    """

    @patch.object(DataStore, "_execute_query")
    def test_create_config_definition(self, mock_execute_query):
        """
        Test that the function creates a new configuration definition.

        This test verifies that the function creates a new configuration definition, and also verifies the creation of the internal table and indexes.
        """

        config_key = "sample_config"
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
        }
        primary_key_field = "name"
        secondary_index = "date"
        secondary_indexes_list = [secondary_index]

        creation_query = c_config_definition_query(config_key, primary_key_field)
        internal_query = internal_c_definition_query(
            config_key, schema, primary_key_field, secondary_indexes_list
        )
        index_query = c_index_query(config_key, secondary_index)

        c_config_definition(
            config_key, schema, primary_key_field, secondary_indexes_list
        )

        mock_execute_query.assert_any_call(creation_query)
        mock_execute_query.assert_any_call(internal_query)
        mock_execute_query.assert_any_call(index_query)

    @patch.object(
        DataStore,
        "_execute_query",
        return_value=[{"json_schema": '{"type": "object"}'}],
    )
    def test_retrieve_config_definition(self, mock_execute_query):
        """
        Test that the function retrieves a configuration definition.

        This test verifies that the function retrieves a configuration definition from the internal table.
        """

        config_key = "sample_config"

        internal_query = r_config_definition_query(config_key)
        r_config_definition(config_key)

        mock_execute_query.assert_called_once_with(internal_query, mode="retrieve")

    @patch("app.utils.config_definitions.utils.r_config_definition")
    @patch.object(DataStore, "_execute_query")
    def test_update_config_definition(
        self, mock_execute_query, mock_r_config_definition
    ):
        """
        Test that the function updates a configuration definition.

        This test verifies that the function updates a configuration definition in the internal table, and also verifies the creation and deletion of indexes.
        """

        config_key = "sample_config"
        updated_indexes_list = ["name"]

        mock_r_config_definition.return_value = {
            "json_schema": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
            },
            "primary_key": "name",
            "secondary_indexes": ["date"],
        }

        internal_query = internal_u_definition_query(config_key, updated_indexes_list)
        index_list_query = l_index_query(config_key)
        index_creation_query = c_index_query(config_key, "name")
        index_deletion_query = d_index_query(config_key, "date")

        def side_effect(query, mode=None):
            if query == index_list_query and mode == "retrieve":
                return [{"indexname": "date"}]
            return []

        mock_execute_query.side_effect = side_effect

        u_config_definition(config_key, updated_indexes_list)

        mock_execute_query.assert_any_call(index_list_query, mode="retrieve")
        mock_execute_query.assert_any_call(index_creation_query)
        mock_execute_query.assert_any_call(index_deletion_query)

        mock_r_config_definition.assert_called_once_with(config_key)
        mock_execute_query.assert_any_call(internal_query)

    @patch.object(DataStore, "_execute_query")
    def test_delete_config_definition(self, mock_execute_query):
        """
        Test that the function deletes a configuration definition.

        This test verifies that the function deletes a configuration definition from the internal table.
        """

        config_key = "sample_config"

        delete_query = d_config_definition_query(config_key)
        internal_query = internal_d_definition_query(config_key)
        d_config_definition(config_key)

        mock_execute_query.assert_any_call(delete_query)
        mock_execute_query.assert_any_call(internal_query)

    @patch.object(
        DataStore, "_execute_query", return_value=[{"config_key": "sample_config"}]
    )
    def test_list_config_definitions(self, mock_execute_query):
        """
        Test that the function lists configuration definitions.

        This test verifies that the function lists configuration definitions from the internal table.
        """

        page_number = 1
        items_per_page = 10

        internal_query = l_config_definition_query(page_number, items_per_page)
        l_config_definition(page_number, items_per_page)

        mock_execute_query.assert_called_once_with(internal_query, mode="retrieve")
