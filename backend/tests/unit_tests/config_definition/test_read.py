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

    from app.utils.config_definitions.utils import r_config_definition

from app.utils.config_definitions.queries import r_config_definition_query

from app.utils.exceptions.errors import APIError

from tests.unit_tests.config_definition.payloads.payload_extractor import (
    extract_payload,
    extract_payload_params,
)


class TestConfigDefinitionRead:
    """
    Unit tests for the read functions of the configuration definition module.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["read"]

    def _run_r_config_definition(self, payload_extract, mock_execute_query):
        """
        Helper function to run r_config_definition and handle assertions.
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

        if expected_error:
            with pytest.raises(APIError) as error:
                r_config_definition(config_key)
            detail = error.value.detail[0]
            assert detail["msg"] == expected_error
            mock_execute_query.assert_not_called()
            return

        mock_execute_query.return_value = return_value
        internal_query, internal_params = r_config_definition_query(config_key)

        r_config_definition(config_key)

        mock_execute_query.assert_called_once_with(
            internal_query, params=internal_params, mode="retrieve"
        )

    @patch.object(DataStore, "execute_query")
    def test_read_w_key(self, mock_execute_query, get_payload):
        """
        Test that the function retrieves a configuration definition with a given key.
        """
        payload_extract = get_payload["test_read_w_key"]
        self._run_r_config_definition(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_read_o_key(self, mock_execute_query, get_payload):
        """
        Test that the function raises an API Error if the config key is not given.
        """
        payload_extract = get_payload["test_read_o_key"]
        self._run_r_config_definition(payload_extract, mock_execute_query)
