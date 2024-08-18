"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.utils.config_definitions.utils import (
    c_config_definition,
    d_config_definition,
)

client = TestClient(app)


class TestConfigDefinitionIntegration:
    """
    Integration test suite for configuration definition endpoints.
    """

    @pytest.fixture(scope="class")
    def setup_data(self):
        """
        Fixture to set up and tear down test data for integration tests.

        This fixture creates a new configuration definition before the tests and deletes it after the tests.
        """

        config_key = "test_config"
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
        }
        primary_key = "name"
        secondary_indexes = ["date"]

        c_config_definition(config_key, schema, primary_key, secondary_indexes)

        yield {
            "config_key": config_key,
            "schema": schema,
            "primary_key": primary_key,
            "secondary_indexes": secondary_indexes,
        }

        d_config_definition(config_key)

    def test_create_config_definition(self):
        """
        Test the creation of a new configuration definition.

        This test verifies that a new configuration definition is created successfully.
        """

        payload = {
            "config_definition_key": "new_config",
            "json_schema": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "date": {"type": "string"}},
            },
            "primary_key": "name",
            "secondary_indexes": ["date"],
        }

        response = client.post("/api/v1/config_definition/", json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "message": "Configuration definition created successfully."
        }

        d_config_definition("new_config")

    def test_get_config_definition(self, setup_data):
        """
        Test retrieval of a configuration definition.

        This test verifies that a configuration definition is retrieved successfully.
        """

        response = client.get(f"/api/v1/config_definition/{setup_data['config_key']}")
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == "Configuration definition retrieved successfully."
        )
        assert "data" in response.json()

    def test_update_config_definition(self, setup_data):
        """
        Test the update of an existing configuration definition.

        This test verifies that an existing configuration definition is updated successfully.
        """

        payload = {"secondary_indexes": ["name"]}

        response = client.put(
            f"/api/v1/config_definition/{setup_data['config_key']}", json=payload
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Configuration definition updated successfully."
        }

    def test_delete_config_definition(self, setup_data):
        """
        Test deletion of a configuration definition.

        This test verifies that a configuration definition is deleted successfully.
        """

        response = client.delete(
            f"/api/v1/config_definition/{setup_data['config_key']}"
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Configuration definition deleted successfully."
        }

    def test_list_config_definitions(self):
        """
        Test listing of all configuration definitions.

        This test verifies that all configuration definitions are listed successfully.
        """

        response = client.get("/api/v1/config_definition/?page=1&limit=10")
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == "Configuration definitions listed successfully."
        )
        assert "data" in response.json()
