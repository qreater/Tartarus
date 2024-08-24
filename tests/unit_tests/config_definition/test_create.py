"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock

import pytest

from app.utils.data.data_source import DataStore

with patch("app.utils.data.data_source.connect") as mock_connect:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    from app.utils.config_definitions.utils import (
        c_config_definition,
    )

from app.utils.config_definitions.queries import (
    c_config_definition_query,
    internal_c_definition_query,
    c_index_query,
)


class TestConfigDefinitionCreate:
    """
    Test suite for the config definition creation functions.
    """

    @patch.object(DataStore, "_execute_query")
    def test_create_w_schema(self, mock_execute_query):
        """
        Test that the function creates a new configuration definition.
        """
        config_key = "sample_config"
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
        }
        index = "date"
        indexes_list = [index]

        creation_query, creation_params = c_config_definition_query(config_key)
        internal_query, internal_params = internal_c_definition_query(
            config_key, schema, indexes_list
        )
        index_query, index_params = c_index_query(config_key, index)

        c_config_definition(config_key, schema, indexes_list)

        mock_execute_query.assert_any_call(creation_query, creation_params)
        mock_execute_query.assert_any_call(internal_query, internal_params)
        mock_execute_query.assert_any_call(index_query, index_params)

    @patch.object(DataStore, "_execute_query")
    def test_create_o_schema(self, mock_execute_query):
        """
        Test that the function creates a new configuration definition.
        """
        config_key = "sample_config"
        index = "date"
        indexes_list = [index]

        creation_query, creation_params = c_config_definition_query(config_key)
        internal_query, internal_params = internal_c_definition_query(
            config_key, None, indexes_list
        )
        index_query, index_params = c_index_query(config_key, index)

        c_config_definition(config_key, None, indexes_list)

        mock_execute_query.assert_any_call(creation_query, creation_params)
        mock_execute_query.assert_any_call(internal_query, internal_params)
        mock_execute_query.assert_any_call(index_query, index_params)

    @patch.object(DataStore, "_execute_query")
    def test_create_n_schema(self, mock_execute_query):
        """
        Test that the function raises an exception if the schema is invalid.
        """
        config_key = "sample_config"
        schema = {"type": "string"}
        index = "date"
        indexes_list = [index]

        with pytest.raises(ValueError):
            c_config_definition(config_key, schema, indexes_list)
        mock_execute_query.assert_not_called()

    @patch.object(DataStore, "_execute_query")
    def test_create_d_index(self, mock_execute_query):
        """
        Test that the function raises an exception if the index is duplicated.
        """
        config_key = "sample_config"
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
        }
        index = "date"
        indexes_list = [index, index]

        with pytest.raises(ValueError):
            c_config_definition(config_key, schema, indexes_list)
        mock_execute_query.assert_not_called()

    @patch.object(DataStore, "_execute_query")
    def test_create_n_index(self, mock_execute_query):
        """
        Test that the function raises an exception if the index is not in the schema.
        """
        config_key = "sample_config"
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
        }
        index = "age"
        indexes_list = [index]

        with pytest.raises(ValueError):
            c_config_definition(config_key, schema, indexes_list)
        mock_execute_query.assert_not_called()
