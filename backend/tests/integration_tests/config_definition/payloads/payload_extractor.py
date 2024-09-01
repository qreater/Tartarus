"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import os
import json


def extract_payload():
    """
    Extracts the test payload from the payload file.

    -- Returns
    dict
        The test payload.
    """
    payload_path = os.path.join(os.path.dirname(__file__), "payloads.json")

    with open(payload_path, "r") as file:
        payload = json.load(file)

    return payload


def extract_payload_params(payload):
    """
    Extracts the test parameters from the test payload.

    -- Parameters
    test_payload: dict
        The test payload.

    -- Returns
    tuple
        The test parameters.
    """

    method = payload.get("method")
    url = payload.get("url")
    headers = payload.get("headers")

    json_payload = payload.get("payload")
    query_params = payload.get("query")

    expected_status = payload.get("expected_status")
    expected_response = payload.get("expected_response")

    return (
        method,
        url,
        headers,
        json_payload,
        query_params,
        expected_status,
        expected_response,
    )
