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
        l_config,
    )

from tests.unit_tests.config.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)


class TestConfigList:
    """
    Test suite for the config listing functions.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["list"]

    def _run_l_config(
        self,
        payload_extract,
        mock_execute_query,
        expect_error=False,
    ):
        """
        Helper function to run l_config and handle assertions.
        """
        (config_definition_key, _, data, schema, return_value) = extract_payload_params(
            payload_extract
        )

        mock_execute_query.side_effect = [schema, return_value]

        page = data.get("page")
        page_size = data.get("page_size")

        if expect_error:
            with pytest.raises(ValueError):
                l_config(config_definition_key, page, page_size)
                mock_execute_query.assert_not_called()
            return

        l_config(config_definition_key, page, page_size)
        assert mock_execute_query.call_count == 2

    @patch.object(DataStore, "execute_query")
    def test_list_w_cd_key(self, mock_execute_query, get_payload):
        """
        Test that the function returns a list of configurations for a given configuration definition.
        """
        payload_extract = get_payload["test_list_w_cd_key"]
        self._run_l_config(payload_extract, mock_execute_query)

    @patch.object(DataStore, "execute_query")
    def test_list_o_cd_key(self, mock_execute_query, get_payload):
        """
        Test that the function raises an error when a configuration definition is not found.
        """
        payload_extract = get_payload["test_list_o_cd_key"]
        self._run_l_config(
            payload_extract,
            mock_execute_query,
            expect_error=True,
        )

    @patch.object(DataStore, "execute_query")
    def test_list_n_page(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when given an invalid page number.
        """
        payload_extract = get_payload["test_list_n_page"]
        self._run_l_config(payload_extract, mock_execute_query, expect_error=True)

    @patch.object(DataStore, "execute_query")
    def test_list_n_nlimit(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when given an invalid page size.
        """
        payload_extract = get_payload["test_list_n_nlimit"]
        self._run_l_config(payload_extract, mock_execute_query, expect_error=True)

    @patch.object(DataStore, "execute_query")
    def test_list_n_plimit(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when given an excessive page size.
        """
        payload_extract = get_payload["test_list_n_plimit"]
        self._run_l_config(payload_extract, mock_execute_query, expect_error=True)
