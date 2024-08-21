"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock

from app.utils.data.data_source import DataStore
from app.utils.config_definitions.utils import (
    d_config_definition,
    internal_d_definition_query,
    d_config_definition,
)
from app.utils.config_definitions.queries import d_config_definition_query


class TestConfigDefintionUnitDelete:
    """
    Unit tests for the delete functions of the configuration definition module.
    """

    @patch.object(DataStore, "_execute_query")
    def test_delete_w_key(self, mock_execute_query):
        """
        Test that the function deletes a configuration definition.

        This test verifies that the function deletes a configuration definition from the internal table.
        """

        config_key = "sample_config"

        delete_query, delete_params = d_config_definition_query(config_key)
        internal_query, internal_params = internal_d_definition_query(config_key)
        d_config_definition(config_key)

        mock_execute_query.assert_any_call(delete_query, delete_params)
        mock_execute_query.assert_any_call(internal_query, internal_params)

    @patch.object(DataStore, "_execute_query")
    def test_delete_o_key(self, mock_execute_query):
        """
        Test that the function deletes a configuration definition with no key.

        This test verifies that the function deletes a configuration definition from the internal table without a key.
        """

        config_key = ""

        delete_query, delete_params = d_config_definition_query(config_key)
        internal_query, internal_params = internal_d_definition_query(config_key)
        d_config_definition(config_key)

        mock_execute_query.assert_any_call(delete_query, delete_params)
        mock_execute_query.assert_any_call(internal_query, internal_params)
