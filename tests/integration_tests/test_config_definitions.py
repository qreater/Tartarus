import pytest
from fastapi import testclient
from main import app


@pytest.fixture
def client():
    return testclient.TestClient(app)


def test_create_config_definition(client):
    response = client.post(
        "/api/v1/config_definitions/",
        json={
            "config_definition_key": "test_config_definition",
            "json_schema": {
                "type": "object",
                "properties": {"test_key": {"type": "string"}},
            },
            "primary_key": "test_key",
            "secondary_indexes": ["test_key"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Configuration definition created successfully."
    }


def test_get_config_definition(client):
    response = client.get("/api/v1/config_definitions/test_config_definition")

    assert response.status_code == 200
    assert response.json() == {
        "config_definition_key": "test_config_definition",
        "json_schema": {
            "type": "object",
            "properties": {"test_key": {"type": "string"}},
        },
        "primary_key": "test_key",
        "secondary_indexes": ["test_key"],
    }


def test_update_config_definition(client):
    response = client.put(
        "/api/v1/config_definitions/test_config_definition",
        json={
            "json_schema": {
                "type": "object",
                "properties": {
                    "test_key": {"type": "string"},
                    "new_key": {"type": "string"},
                },
            },
            "primary_key": "test_key",
            "secondary_indexes": ["test_key"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Configuration definition updated successfully."
    }


def test_delete_config_definition(client):
    response = client.delete("/api/v1/config_definitions/test_config_definition")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Configuration definition deleted successfully."
    }


def test_list_config_definitions(client):
    response = client.get("/api/v1/config_definitions/list")

    assert response.status_code == 200
    assert response.json() == {"data": []}
