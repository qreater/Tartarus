"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest

from tests.conftest import (
    API_KEY,
    API_URL,
)
from tests.payloads.payload_extractor import (
    extract_payload_params,
    extract_payload,
)
from tartarus_lib.core import TartarusAPIClient


class TestConfigClient:
    """
    Integration test suite for configuration endpoints.
    """

    @pytest.fixture(scope="class")
    def get_payload(self):
        """
        Extracts the test payload from the payload file for the test suite.
        """
        payload = extract_payload()

        yield payload

    @pytest.fixture(scope="class")
    def get_client(self, get_payload):
        """
        Creates a new client for the test suite.
        """

        client = TartarusAPIClient(API_URL, API_KEY)

        cd_client = client.config_definitions
        c_client = client.configs

        payload = get_payload["pre_c_test"]["payload"]

        cd_client.create(**payload)
        yield c_client
        cd_client.delete(payload["config_definition_key"])

    def _run_test(self, payload_extract, client):
        """
        Helper method to run the test based on the provided test name.
        """

        (
            method,
            payload,
            query,
            expected_response,
        ) = extract_payload_params(payload_extract)

        response = getattr(client, method)(**payload, **query)

        assert response["status"] == "SUCCESS"

        if not expected_response:
            return

        base_keys = ["created_at", "modified_at"]

        for base_key in base_keys:
            response["data"].pop(base_key, None)

        assert response["data"] == expected_response

    def test_c_create(self, get_payload, get_client):
        """
        Test the creation of a new configuration.
        """
        payload_extract = get_payload["test_c_create"]
        self._run_test(payload_extract, get_client)

    def test_c_retrieve(self, get_payload, get_client):
        """
        Test the retrieval of a configuration.
        """
        payload_extract = get_payload["test_c_retrieve"]
        self._run_test(payload_extract, get_client)

    def test_c_update(self, get_payload, get_client):
        """
        Test updating of a configuration.
        """
        payload_extract = get_payload["test_c_update"]
        self._run_test(payload_extract, get_client)

    def test_c_list(self, get_payload, get_client):
        """
        Test listing of configurations.
        """
        payload_extract = get_payload["test_c_list"]
        self._run_test(payload_extract, get_client)

    def test_c_delete(self, get_payload, get_client):
        """
        Test deletion of a configuration.
        """
        payload_extract = get_payload["test_c_delete"]
        self._run_test(payload_extract, get_client)
