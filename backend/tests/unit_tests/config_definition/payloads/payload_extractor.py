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
    config_key = payload.get("config_key")
    schema = payload.get("schema")

    index = payload.get("index")
    indexes = payload.get("indexes")

    params = payload.get("params")

    return_value = payload.get("return_value")
    expected_error = payload.get("expected_error")

    return (
        config_key,
        schema,
        index,
        indexes,
        params,
        return_value,
        expected_error,
    )
