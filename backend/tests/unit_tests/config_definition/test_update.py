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

    from app.utils.config_definitions.utils import u_config_definition

from app.utils.config_definitions.queries import (
    internal_u_definition_query,
    l_index_query,
    c_index_query,
    d_index_query,
)

from tests.unit_tests.config_definition.payloads.payload_extractor import (
    extract_payload,
    extract_payload_params,
)


class TestConfigDefinitionUpdate:
    """
    Unit tests for the update functions of the configuration definition module.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["update"]

    def _run_u_config_definition(
        self,
        payload_extract,
        mock_execute_query,
        mock_r_config_definition,
        expect_error=False,
    ):
        """
        Helper function to run u_config_definition and handle assertions.
        """

        (
            config_key,
            _,
            _,
            updated_indexes_list,
            _,
            _,
        ) = extract_payload_params(payload_extract)

        if expect_error:
            with pytest.raises(ValueError):
                u_config_definition(config_key, updated_indexes_list)
            mock_execute_query.assert_not_called()
            return

        mock_r_config_definition.return_value = {
            "json_schema": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
            },
            "indexes": ["date"],
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
    def test_update_w_index(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function updates a configuration definition.
        """
        payload_extract = get_payload["test_update_w_index"]

        self._run_u_config_definition(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
            expect_error=False,
        )

    @patch("app.utils.config_definitions.utils.r_config_definition")
    @patch.object(DataStore, "_execute_query")
    def test_update_d_index(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function raises an exception if the secondary index is duplicated.
        """
        payload_extract = get_payload["test_update_d_index"]

        self._run_u_config_definition(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
            expect_error=True,
        )

    @patch("app.utils.config_definitions.utils.r_config_definition")
    @patch.object(DataStore, "_execute_query")
    def test_update_n_index(self, mock_execute_query, mock_r_config_definition):
        """
        Test that the function raises an exception if the secondary index is not found.
        """
        payload_extract = extract_payload()["update"]["test_update_n_index"]

        self._run_u_config_definition(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
            expect_error=True,
        )
