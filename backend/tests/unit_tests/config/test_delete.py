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
        d_config,
    )

from app.utils.configs.queries import (
    d_config_query,
)

from tests.unit_tests.config.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)


class TestConfigDelete:
    """
    Test suite for the config deletion functions.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["delete"]

    def _run_d_config(
        self,
        payload_extract,
        mock_execute_query,
        expect_error=False,
    ):
        """
        Helper function to run d_config and handle assertions.
        """
        (config_definition_key, config_key, _, _) = extract_payload_params(
            payload_extract
        )

        delete_query, delete_params = d_config_query(config_definition_key, config_key)

        if expect_error:
            with pytest.raises(ValueError):
                d_config(config_definition_key, config_key)
                mock_execute_query.assert_not_called()
            return

        d_config(config_definition_key, config_key)
        mock_execute_query.assert_called_once()

    @patch.object(DataStore, "_execute_query")
    def test_delete_w_key(self, mock_execute_query, get_payload):
        """
        Test the deletion of a configuration with a key.
        """
        payload_extract = get_payload["test_delete_w_key"]
        self._run_d_config(payload_extract, mock_execute_query)

    @patch.object(DataStore, "_execute_query")
    def test_delete_o_key(self, mock_execute_query, get_payload):
        """
        Test the deletion of a configuration without a key.
        """
        payload_extract = get_payload["test_delete_o_key"]
        self._run_d_config(payload_extract, mock_execute_query, expect_error=True)

    @patch.object(DataStore, "_execute_query")
    def test_delete_w_cd_key(self, mock_execute_query, get_payload):
        """
        Test the deletion of a configuration with a key and config definition key.
        """
        payload_extract = get_payload["test_delete_w_cd_key"]
        self._run_d_config(payload_extract, mock_execute_query)

    @patch.object(DataStore, "_execute_query")
    def test_delete_o_cd_key(self, mock_execute_query, get_payload):
        """
        Test the deletion of a configuration without a key and config definition key.
        """
        payload_extract = get_payload["test_delete_o_cd_key"]
        self._run_d_config(payload_extract, mock_execute_query, expect_error=True)