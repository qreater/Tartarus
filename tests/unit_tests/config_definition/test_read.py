"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock

from app.utils.data.data_source import DataStore

with patch("app.utils.data.data_source.connect") as mock_connect:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    from app.utils.config_definitions.utils import r_config_definition

from app.utils.config_definitions.queries import r_config_definition_query


class TestConfigDefintionRead:
    """
    Unit tests for the read functions of the configuration definition module.
    """

    @patch.object(
        DataStore,
        "_execute_query",
        return_value=[{"json_schema": '{"type": "object"}'}],
    )
    def test_read_w_key(self, mock_execute_query):
        """
        Test that the function retrieves a configuration definition.
        """

        config_key = "sample_config"

        internal_query, internal_params = r_config_definition_query(config_key)
        r_config_definition(config_key)

        mock_execute_query.assert_called_once_with(
            internal_query, params=internal_params, mode="retrieve"
        )

    @patch.object(
        DataStore,
        "_execute_query",
        return_value=[{"json_schema": '{"type": "object"}'}],
    )
    def test_read_o_key(self, mock_execute_query):
        """
        Test that the function retrieves a configuration definition if key is not given.
        """

        config_key = ""

        internal_query, internal_params = r_config_definition_query(config_key)
        r_config_definition(config_key)

        mock_execute_query.assert_called_once_with(
            internal_query, params=internal_params, mode="retrieve"
        )
