"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from tartarus_lib.clients.base import BaseAPIClient


class ConfigDefinitionAPI:
    """
    API client for managing configuration definitions.

    Handles creation, retrieval, update, deletion, and listing of config definitions.
    """

    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize the ConfigDefinitionAPI.

        :param base_client: An instance of BaseAPIClient.
        """
        self.base_client = base_client

    def create(
        self, config_definition_key: str, json_schema: dict = None, indexes: list = None
    ):
        """
        Create a new configuration definition.

        :param config_definition_key: The key for the configuration definition.
        :param json_schema: The JSON schema for the configuration definition.
        :param indexes: The list of indexes for the configuration definition.
        """

        data = {
            "config_definition_key": config_definition_key,
            "json_schema": json_schema,
            "indexes": indexes or [],
        }
        return self.base_client._make_request("POST", "config_definition/", json=data)

    def retrieve(self, config_definition_key: str):
        """
        Retrieve a configuration definition by its key.

        :param config_definition_key: The key for the configuration definition.
        """

        endpoint = f"config_definition/{config_definition_key}"
        return self.base_client._make_request("GET", endpoint)

    def update(self, config_definition_key: str, indexes: list):
        """
        Update an existing configuration definition.

        :param config_definition_key: The key for the configuration definition.
        :param indexes: The list of indexes for the configuration definition.
        """

        data = {"indexes": indexes}
        endpoint = f"config_definition/{config_definition_key}"
        return self.base_client._make_request("PUT", endpoint, json=data)

    def delete(self, config_definition_key: str):
        """
        Delete a configuration definition by its key.

        :param config_definition_key: The key for the configuration definition.
        """

        endpoint = f"config_definition/{config_definition_key}"
        return self.base_client._make_request("DELETE", endpoint)

    def list(
        self,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "modified_at",
        sort_order: str = "desc",
        search: str = None,
    ):
        """
        List all configuration definitions.

        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        :param sort_by: The field to sort by.
        :param sort_order: The order to sort by.
        :param search: The search term to filter by.
        """

        params = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }

        if search:
            params["search"] = search
        endpoint = f"config_definition/"
        return self.base_client._make_request("GET", endpoint, params=params)
