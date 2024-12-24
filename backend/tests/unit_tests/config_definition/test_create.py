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

    from app.utils.config_definitions.utils import (
        c_config_definition,
    )

from app.utils.config_definitions.queries import (
    c_config_definition_query,
    internal_c_definition_query,
    c_index_query,
)

from app.utils.exceptions.errors import APIError

from tests.unit_tests.config_definition.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)


class TestConfigDefinitionCreate:
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
    ):
        """
        Helper function to run c_config_definition and handle assertions.
        """
        (
            config_key,
            schema,
            index,
            indexes,
            _,
            _,
            expected_error,
        ) = extract_payload_params(payload_extract)

        if expected_error:
            with pytest.raises(APIError) as error:
                c_config_definition(config_key, schema, indexes)
            detail = error.value.detail[0]
            assert detail["msg"] == expected_error
            return

        creation_query, creation_params = c_config_definition_query(config_key)
        internal_query, internal_params = internal_c_definition_query(
            config_key, schema, indexes
        )
        index_query, index_params = c_index_query(config_key, index)

        c_config_definition(config_key, schema, indexes)

        mock_execute_query.assert_any_call(creation_query, creation_params)
        mock_execute_query.assert_any_call(internal_query, internal_params)
        mock_execute_query.assert_any_call(index_query, index_params)

    @patch.object(DataStore, "execute_query")
    def test_create_w_schema(self, mock_execute_query, get_payload):
        """
        Test that the function creates a new configuration definition with a schema.
        """
        payload_extract = get_payload["test_create_w_schema"]
        self._run_c_config_definition(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_create_o_schema(self, mock_execute_query, get_payload):
        """
        Test that the function creates a new configuration definition without a schema.
        """
        payload_extract = get_payload["test_create_o_schema"]
        self._run_c_config_definition(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_create_n_schema(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception if the schema is invalid.
        """
        payload_extract = get_payload["test_create_n_schema"]
        self._run_c_config_definition(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_create_d_sindex(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception if the index are duplicated.
        """
        payload_extract = get_payload["test_create_d_sindex"]
        self._run_c_config_definition(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_create_n_sindex(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception if the indexes are not in the schema.
        """
        payload_extract = get_payload["test_create_n_sindex"]
        self._run_c_config_definition(payload_extract, mock_execute_query)
