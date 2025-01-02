"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import pytest

from unittest.mock import MagicMock

from tests.conftest import (
    API_KEY,
    API_URL,
)
from tartarus_lib.core import TartarusAPIClient


@pytest.fixture
def mock_base_client():
    """
    Create a mock BaseAPIClient instance.

    :return: A mock BaseAPIClient instance.
    """
    client = MagicMock(spec=TartarusAPIClient)

    client.base_url = API_URL
    client.api_key = API_KEY

    return client


def test_client():
    """
    Test the TartarusAPIClient class.
    """
    client = TartarusAPIClient(base_url=API_URL, api_key=API_KEY)

    assert client.configs is not None
    assert client.config_definitions is not None

    assert client.ping() == {"message": "Welcome to Tartarus API"}
