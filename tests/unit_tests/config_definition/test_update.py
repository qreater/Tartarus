"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock
import pytest

from app.utils.data.data_source import DataStore
from app.utils.config_definitions.utils import (
    u_config_definition,
    internal_u_definition_query,
    c_index_query,
    d_index_query,
    l_index_query,
)


class TestConfigDefintionUpdate:
    """
    Unit tests for the update functions of the configuration definition module.
    """

    @patch("app.utils.config_definitions.utils.r_config_definition")
    @patch.object(DataStore, "_execute_query")
    def test_update_w_sindex(self, mock_execute_query, mock_r_config_definition):
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

        internal_query, internal_params = internal_u_definition_query(
            config_key, updated_indexes_list
        )
        index_list_query, index_list_params = l_index_query(config_key)
        index_creation_query, index_creation_params = c_index_query(config_key, "name")
        index_deletion_query, index_deletion_params = d_index_query(config_key, "date")

        def side_effect(query, params=None, mode=None):
            if (
                query == index_list_query
                and params == index_list_params
                and mode == "retrieve"
            ):
                return [{"indexname": "date"}]
            return []

        mock_execute_query.side_effect = side_effect

        u_config_definition(config_key, updated_indexes_list)

        mock_execute_query.assert_any_call(
            index_list_query, params=index_list_params, mode="retrieve"
        )
        mock_execute_query.assert_any_call(index_creation_query, index_creation_params)
        mock_execute_query.assert_any_call(index_deletion_query, index_deletion_params)

        mock_r_config_definition.assert_called_once_with(config_key)
        mock_execute_query.assert_any_call(internal_query, internal_params)

    @patch("app.utils.config_definitions.utils.r_config_definition")
    @patch.object(DataStore, "_execute_query")
    def test_update_d_sindex(self, mock_execute_query, mock_r_config_definition):
        """
        Test that the function raises an exception if the secondary index is duplicated.
        """
        mock_r_config_definition.return_value = {
            "json_schema": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
            },
            "primary_key": "name",
            "secondary_indexes": ["date"],
        }

        config_key = "sample_config"
        updated_indexes_list = ["name", "name"]

        with pytest.raises(ValueError):
            u_config_definition(config_key, updated_indexes_list)
        mock_execute_query.assert_not_called()

    @patch("app.utils.config_definitions.utils.r_config_definition")
    @patch.object(DataStore, "_execute_query")
    def test_update_n_sindex(self, mock_execute_query, mock_r_config_definition):
        """
        Test that the function raises an exception if the secondary index is not found.
        """
        mock_r_config_definition.return_value = {
            "json_schema": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
            },
            "primary_key": "name",
            "secondary_indexes": ["date"],
        }

        config_key = "sample_config"
        updated_indexes_list = ["dog"]

        with pytest.raises(ValueError):
            u_config_definition(config_key, updated_indexes_list)
        mock_execute_query.assert_not_called()
