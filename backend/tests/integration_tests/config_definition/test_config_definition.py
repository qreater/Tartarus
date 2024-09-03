"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest
from fastapi.testclient import TestClient
from main import app

from app.utils.settings.config import settings

from tests.integration_tests.config_definition.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)

client = TestClient(app)


class TestConfigDefinitionIntegration:
    """
    Integration test suite for configuration definition endpoints.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        return extract_payload()

    def _run_test(self, payload_extract):
        """
        Helper method to run the test based on the provided test name.
        """

        (
            method,
            url,
            headers,
            json_payload,
            query_params,
            expected_status,
            expected_response,
        ) = extract_payload_params(payload_extract)
        headers = {"Authorization": settings.API_KEY}

        response = client.request(
            method, url, headers=headers, params=query_params, json=json_payload
        )

        assert response.status_code == expected_status
        if expected_response:
            assert response.json() == expected_response

    def test_create_config_definition(self, get_payload):
        """
        Test the creation of a new configuration definition.
        """
        payload_extract = get_payload["test_create_config_definition"]
        self._run_test(payload_extract)

    def test_get_config_definition(self, get_payload):
        """
        Test retrieval of a configuration definition.
        """
        payload_extract = get_payload["test_get_config_definition"]
        self._run_test(payload_extract)

    def test_update_config_definition(self, get_payload):
        """
        Test the update of an existing configuration definition.
        """
        payload_extract = get_payload["test_update_config_definition"]
        self._run_test(payload_extract)

    def test_delete_config_definition(self, get_payload):
        """
        Test the deletion of a configuration definition.
        """
        payload_extract = get_payload["test_delete_config_definition"]
        self._run_test(payload_extract)

    def test_list_config_definitions(self, get_payload):
        """
        Test listing of all configuration definitions.
        """
        payload_extract = get_payload["test_list_config_definitions"]
        self._run_test(payload_extract)
