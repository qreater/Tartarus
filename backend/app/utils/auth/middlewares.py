"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from fastapi import Header, HTTPException


def validate_api_key(x_api_key: str = Header(None)):
    """
    Validate the API key.
    """
    if not x_api_key:
        raise HTTPException(status_code=403, detail="API key missing")
