"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import requests
from tartarus_lib.exceptions import TartarusError


class BaseAPIClient:
    """
    Base class for handling API interactions.

    Provides methods for making authenticated HTTP requests.
    """

    def __init__(
        self, base_url: str, api_key: str, version: str = "v1", timeout: int = 10
    ):
        """
        Initialize the BaseAPIClient.

        :param base_url: The base URL of the API.
        :param api_key: The API key for authentication.
        :param version: The API version to use (default: v1).
        :param timeout: Timeout for API requests (default: 10 seconds).
        """
        self.base_url = base_url.rstrip("/")
        self.version = version
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key})

    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Send an HTTP request to the API.

        :param method: HTTP method (GET, POST, etc.).
        :param endpoint: API endpoint relative to the base URL.
        :param kwargs: Additional parameters for the request.

        :return: JSON response from the API.
        :raises TartarusError: If the request fails.
        """
        if endpoint in ("/", "/health"):
            url = f"{self.base_url}{endpoint}"
        else:
            url = f"{self.base_url}/api/{self.version}/{endpoint.lstrip('/')}{kwargs.pop('url_suffix', '')}"
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_message = f"API request failed: {e}"
            if isinstance(e, requests.HTTPError) and e.response is not None:
                error_message += f"\nResponse Body: {e.response.text}"
            raise TartarusError(error_message) from e
