"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch, MagicMock

import pytest

from app.utils.data.data_source import DataStore
from app.utils.exceptions.errors import APIError

with patch("app.utils.data.data_source.connect") as mock_connect:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    from app.utils.configs.utils import (
        c_config,
    )

from tests.unit_tests.config.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)


class TestConfigCreate:
    """
    Test suite for the config creation functions.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["create"]

    def _run_c_config(
        self, payload_extract, mock_execute_query, mock_r_config_definition
    ):
        """
        Helper function to run c_config and handle assertions.
        """
        (
            config_definition_key,
            config_key,
            data,
            schema,
            _,
            expected_error,
        ) = extract_payload_params(payload_extract)

        mock_r_config_definition.return_value = schema

        if expected_error:
            with pytest.raises(APIError) as error:
                c_config(config_definition_key, config_key, data)
            detail = error.value.detail[0]
            assert detail["msg"] == expected_error
            return

        c_config(config_definition_key, config_key, data)
        assert mock_execute_query.call_count == 2

    @patch("app.utils.configs.validations.r_config_definition")
    @patch.object(DataStore, "execute_query")
    def test_create_w_schema(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function creates a new configuration with schema.
        """
        payload_extract = get_payload["test_create_w_schema"]
        self._run_c_config(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
        )

    @patch("app.utils.configs.validations.r_config_definition")
    @patch.object(DataStore, "execute_query")
    def test_create_o_schema(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function creates a new configuration without a schema.
        """
        payload_extract = get_payload["test_create_o_schema"]
        self._run_c_config(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
        )

    @patch("app.utils.configs.validations.r_config_definition")
    @patch.object(DataStore, "execute_query")
    def test_create_n_schema(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function raises an exception if the schema is invalid.
        """
        payload_extract = get_payload["test_create_n_schema"]
        self._run_c_config(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
        )
