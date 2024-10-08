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

    from app.utils.config_definitions.utils import l_config_definition

from app.utils.config_definitions.queries import l_config_definition_query

from tests.unit_tests.config_definition.payloads.payload_extractor import (
    extract_payload,
    extract_payload_params,
)


class TestConfigDefinitionList:
    """
    Unit tests for the list functions of the configuration definition module.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()["list"]

    def _run_l_config_definition(
        self,
        payload_extract,
        mock_execute_query,
        expect_error=False,
    ):
        """
        Helper function to run l_config_definition and handle assertions.
        """
        (
            _,
            _,
            _,
            _,
            page_number,
            items_per_page,
            return_value,
        ) = extract_payload_params(payload_extract)

        if expect_error:
            with pytest.raises(ValueError):
                l_config_definition(page_number, items_per_page)
            mock_execute_query.assert_not_called()
            return

        mock_execute_query.return_value = return_value
        internal_query, internal_params = l_config_definition_query(
            page_number, items_per_page
        )

        l_config_definition(page_number, items_per_page)

        mock_execute_query.assert_called_once_with(
            internal_query, params=internal_params, mode="retrieve"
        )

    @patch.object(DataStore, "execute_query")
    def test_list_w_params(self, mock_execute_query, get_payload):
        """
        Test that the function lists configuration definitions with a valid page number and items per page.
        """
        payload_extract = get_payload["test_list_w_params"]
        self._run_l_config_definition(
            payload_extract, mock_execute_query, expect_error=False
        )

    @patch.object(DataStore, "execute_query")
    def test_list_n_page(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when given an invalid page number.
        """
        payload_extract = get_payload["test_list_n_page"]
        self._run_l_config_definition(
            payload_extract, mock_execute_query, expect_error=True
        )

    @patch.object(DataStore, "execute_query")
    def test_list_n_nlimit(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when given an invalid page size.
        """
        payload_extract = get_payload["test_list_n_nlimit"]
        self._run_l_config_definition(
            payload_extract, mock_execute_query, expect_error=True
        )

    @patch.object(DataStore, "execute_query")
    def test_list_n_plimit(self, mock_execute_query, get_payload):
        """
        Test that the function raises an exception when given an excessive page size.
        """
        payload_extract = get_payload["test_list_n_plimit"]
        self._run_l_config_definition(
            payload_extract, mock_execute_query, expect_error=True
        )
