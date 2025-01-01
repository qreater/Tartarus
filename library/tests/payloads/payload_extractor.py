"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import os
import json


def extract_payload() -> dict:
    """
    Extracts the test payload from the payload file.

    :return: dict
    """
    payload_path = os.path.join(os.path.dirname(__file__), "payloads.json")

    with open(payload_path, "r") as file:
        payload = json.load(file)

    return payload


def extract_payload_params(payload: dict) -> tuple:
    """
    Extracts the test parameters from the test payload.

    :param payload: dict
    :return: tuple
    """

    method = payload.get("method")
    json_payload = payload.get("payload", {})
    query_params = payload.get("query", {})

    response = payload.get("response")

    return (
        method,
        json_payload,
        query_params,
        response,
    )
