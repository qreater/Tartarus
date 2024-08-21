"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from unittest.mock import patch
import pytest

from app.utils.data.data_source import DataStore
from app.utils.config_definitions.utils import (
    l_config_definition,
)
from app.utils.config_definitions.queries import (
    l_config_definition_query,
)


class TestConfigDefintionList:
    """
    Unit tests for the list functions of the configuration definition module.
    """

    @patch.object(DataStore, "_execute_query")
    def test_list_w_params(self, mock_execute_query):
        """
        Test that the function lists configuration definitions with a page number.

        This test verifies that the function lists configuration definitions from the internal table with a page number.
        """

        page_number = 1
        items_per_page = 10

        internal_query, internal_params = l_config_definition_query(
            page_number, items_per_page
        )
        l_config_definition(page_number, items_per_page)

        mock_execute_query.assert_called_once_with(
            internal_query, params=internal_params, mode="retrieve"
        )

    @patch.object(DataStore, "_execute_query")
    def test_list_o_params(self, mock_execute_query):
        """
        Test that the function lists configuration definitions with no parameters.

        This test verifies that the function lists configuration definitions from the internal table without any parameters.
        """
        internal_query, internal_params = l_config_definition_query()
        l_config_definition()

        mock_execute_query.assert_called_once_with(
            internal_query, params=internal_params, mode="retrieve"
        )

    @patch.object(DataStore, "_execute_query")
    def test_list_n_page(self, mock_execute_query):
        """
        Test that the function lists configuration definitions with an invalid page number.

        This test verifies that the function lists configuration definitions from the internal table with an invalid page number.
        """
        page_number = -1
        items_per_page = 10

        with pytest.raises(ValueError):
            l_config_definition(page_number, items_per_page)

        mock_execute_query.assert_not_called()

    @patch.object(DataStore, "_execute_query")
    def test_list_n_nlimit(self, mock_execute_query):
        """
        Test that the function lists configuration definitions with an invalid page size.

        This test verifies that the function lists configuration definitions from the internal table with an invalid page size.
        """
        page_number = 1
        items_per_page = -1

        with pytest.raises(ValueError):
            l_config_definition(page_number, items_per_page)

        mock_execute_query.assert_not_called()

    @patch.object(DataStore, "_execute_query")
    def test_list_n_plimit(self, mock_execute_query):
        """
        Test that the function lists configuration definitions with an exceed page size.

        This test verifies that the function lists configuration definitions from the internal table with an exceed page size.
        """
        page_number = 1
        items_per_page = 101

        with pytest.raises(ValueError):
            l_config_definition(page_number, items_per_page)

        mock_execute_query.assert_not_called()
