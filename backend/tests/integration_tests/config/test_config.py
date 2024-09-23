"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest
from fastapi.testclient import TestClient
from main import app

from app.utils.settings.config import settings
from app.utils.config_definitions.utils import c_config_definition, d_config_definition

from tests.integration_tests.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)

client = TestClient(app)


class TestConfigIntegration:
    """
    Integration test suite for configuration definition endpoints.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        payload = extract_payload()
        pre_payload = payload.get("pre_test_config")

        c_config_definition(**pre_payload)
        yield payload
        d_config_definition(pre_payload.get("config_definition_key"))

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

    def test_create_config(self, get_payload):
        """
        Test the creation of a new configuration.
        """
        payload_extract = get_payload["test_create_config"]
        self._run_test(payload_extract)

    def test_delete_config(self, get_payload):
        """
        Test deletion of a configuration.
        """
        payload_extract = get_payload["test_delete_config"]
        self._run_test(payload_extract)
