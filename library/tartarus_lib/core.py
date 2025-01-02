"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from tartarus_lib.clients.base import BaseAPIClient
from tartarus_lib.clients.config_definition import ConfigDefinitionAPI
from tartarus_lib.clients.config import ConfigAPI


class TartarusAPIClient:
    """
    Client for interacting with the Tartarus API.

    Combines configuration definition and configuration management functionalities.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the TartarusAPIClient.

        :param base_url: The base URL of the Tartarus API.
        :param api_key: The API key for authentication.
        """
        self.base_client = BaseAPIClient(base_url, api_key)
        self.config_definitions = ConfigDefinitionAPI(self.base_client)
        self.configs = ConfigAPI(self.base_client)

    def ping(self):
        """Check if the API is reachable."""
        return self.base_client._make_request("GET", "/")
