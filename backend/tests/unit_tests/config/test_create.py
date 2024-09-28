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
        c_config,
    )

from tests.unit_tests.config.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)


class TestConfigCreate:
    """
    Test suite for the config definition creation functions.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["create"]

    def _run_c_config_definition(
        self,
        payload_extract,
        mock_execute_query,
        mock_r_config_definition,
        expect_error=False,
    ):
        """
        Helper function to run c_config_definition and handle assertions.
        """
        (config_definition_key, config_key, data, schema, _) = extract_payload_params(
            payload_extract
        )

        mock_r_config_definition.return_value = schema

        if expect_error:
            with pytest.raises(ValueError):
                c_config(config_definition_key, config_key, data)
                mock_execute_query.assert_not_called()
            return

        c_config(config_definition_key, config_key, data)
        mock_execute_query.assert_called_once()

    @patch("app.utils.configs.validations.r_config_definition")
    @patch.object(DataStore, "execute_query")
    def test_create_w_schema(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function creates a new configuration definition with a schema.
        """
        payload_extract = get_payload["test_create_w_schema"]
        self._run_c_config_definition(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
            expect_error=False,
        )

    @patch("app.utils.configs.validations.r_config_definition")
    @patch.object(DataStore, "execute_query")
    def test_create_o_schema(
        self, mock_execute_query, mock_r_config_definition, get_payload
    ):
        """
        Test that the function creates a new configuration definition without a schema.
        """
        payload_extract = get_payload["test_create_o_schema"]
        self._run_c_config_definition(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
            expect_error=False,
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
        self._run_c_config_definition(
            payload_extract,
            mock_execute_query,
            mock_r_config_definition,
            expect_error=True,
        )
