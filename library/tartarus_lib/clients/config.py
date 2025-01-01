"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from tartarus_lib.clients.base import BaseAPIClient


class ConfigAPI:
    """
    API client for managing individual configurations.

    Handles creation, retrieval, update, deletion, and listing of configurations under specific definitions.
    """

    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize the ConfigAPI.

        :param base_client: An instance of BaseAPIClient.
        """
        self.base_client = base_client

    def create(self, config_definition_key: str, config_key: str, data: dict):
        """
        Create a new configuration under a specific definition.

        :param config_definition_key: The key for the configuration definition.
        :param config_key: The key for the configuration.
        :param data: The data for the configuration.
        """

        data = {
            "config_key": config_key,
            "data": data,
        }
        endpoint = f"config_definition/{config_definition_key}/config"
        return self.base_client._make_request("POST", endpoint, json=data)

    def retrieve(self, config_definition_key: str, config_key: str):
        """
        Retrieve a configuration by its key.

        :param config_definition_key: The key for the configuration definition.
        :param config_key: The key for the configuration.
        """

        endpoint = f"config_definition/{config_definition_key}/config/{config_key}"
        return self.base_client._make_request("GET", endpoint)

    def update(self, config_definition_key: str, config_key: str, data: dict):
        """
        Update an existing configuration.

        :param config_definition_key: The key for the configuration definition.
        :param config_key: The key for the configuration.
        :param data: The data for the configuration.
        """

        data = {"data": data}
        endpoint = f"config_definition/{config_definition_key}/config/{config_key}"
        return self.base_client._make_request("PUT", endpoint, json=data)

    def delete(self, config_definition_key: str, config_key: str):
        """
        Delete a configuration by its key.

        :param config_definition_key: The key for the configuration definition.
        :param config_key: The key for the configuration.
        """

        endpoint = f"config_definition/{config_definition_key}/config/{config_key}"
        return self.base_client._make_request("DELETE", endpoint)

    def list(
        self,
        config_definition_key: str,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "modified_at",
        sort_order: str = "desc",
        search: str = None,
    ):
        """
        List all configurations under a specific definition.

        :param config_definition_key: The key for the configuration definition.
        :param page: The page number.
        :param limit: The number of configurations to return per page.
        :param sort_by: The field to sort by.
        :param sort_order: The order to sort by.
        :param search: The search term to filter configurations by.
        """

        params = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }

        if search:
            params["search"] = search

        endpoint = f"config_definition/{config_definition_key}/config/"
        return self.base_client._make_request("GET", endpoint, params=params)
