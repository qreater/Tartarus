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

    from app.utils.configs.utils import (
        r_config,
    )

from tests.unit_tests.config.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)


class TestConfigRead:
    """
    Test suite for the config reading functions.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["read"]

    def _run_r_config(
        self,
        payload_extract,
        mock_execute_query,
    ):
        """
        Helper function to run r_config and handle assertions.
        """
        (
            config_definition_key,
            config_key,
            _,
            schema,
            return_value,
            expected_error,
        ) = extract_payload_params(payload_extract)

        mock_execute_query.side_effect = [schema, return_value]

        if expected_error:
            with pytest.raises(ValueError) as error:
                r_config(config_definition_key, config_key)
                mock_execute_query.assert_not_called()
            assert str(error.value) == expected_error
            return

        r_config(config_definition_key, config_key)
        assert mock_execute_query.call_count == 2

    @patch.object(DataStore, "execute_query")
    def test_read_w_key(self, mock_execute_query, get_payload):
        """
        Test that the function retrieves a configuration with valid keys.
        """
        payload_extract = get_payload["test_read_w_key"]
        self._run_r_config(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_read_o_key(self, mock_execute_query, get_payload):
        """
        Test that the function raises an error when a configuration is not found.
        """
        payload_extract = get_payload["test_read_o_key"]
        self._run_r_config(
            payload_extract,
            mock_execute_query,
        )

    @patch.object(DataStore, "execute_query")
    def test_read_o_cd_key(self, mock_execute_query, get_payload):
        """
        Test that the function raises an error when a configuration definition is not found.
        """
        payload_extract = get_payload["test_read_o_cd_key"]
        self._run_r_config(
            payload_extract,
            mock_execute_query,
        )
