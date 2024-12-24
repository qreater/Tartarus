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

    from app.utils.config_definitions.utils import d_config_definition

from app.utils.config_definitions.queries import (
    d_config_definition_query,
    internal_d_definition_query,
)

from app.utils.exceptions.errors import APIError

from tests.unit_tests.config_definition.payloads.payload_extractor import (
    extract_payload,
    extract_payload_params,
)


class TestConfigDefinitionDelete:
    """
    Unit tests for the delete functions of the configuration definition module.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["delete"]

    def _run_d_config_definition(
        self,
        payload_extract,
        mock_execute_query,
    ):
        """
        Helper function to run d_config_definition and handle assertions.
        """
        (
            config_key,
            _,
            _,
            _,
            _,
            return_value,
            expected_error,
        ) = extract_payload_params(payload_extract)

        mock_execute_query.return_value = return_value

        if expected_error:
            with pytest.raises(APIError) as error:
                d_config_definition(config_key)
            detail = error.value.detail[0]
            assert detail["msg"] == expected_error
            mock_execute_query.assert_not_called()
            return

        delete_query, delete_params = d_config_definition_query(config_key)
        internal_query, internal_params = internal_d_definition_query(config_key)

        d_config_definition(config_key)

        mock_execute_query.assert_any_call(delete_query, delete_params)
        mock_execute_query.assert_any_call(internal_query, internal_params)

    @patch.object(DataStore, "execute_query")
    def test_delete_w_key(self, mock_execute_query, get_payload):
        """
        Test that the function deletes a configuration definition with a valid key.
        """
        payload_extract = get_payload["test_delete_w_key"]
        self._run_d_config_definition(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_delete_o_key(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when trying to delete with an empty key.
        """
        payload_extract = get_payload["test_delete_o_key"]
        self._run_d_config_definition(payload_extract, mock_execute_query)
