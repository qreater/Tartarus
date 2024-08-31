"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.config.conf import settings

QUERY_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {settings.INTERNAL_TABLE} (
    config_type_key VARCHAR(255) PRIMARY KEY NOT NULL,
    json_schema JSONB,
    indexes TEXT[]
);
"""

QUERY_CREATE_INDEX = f"""
CREATE INDEX IF NOT EXISTS idx_{settings.DB_NAME}_json_schema
ON {settings.INTERNAL_TABLE} USING gin (json_schema);

CREATE INDEX IF NOT EXISTS idx_{settings.DB_NAME}_indexes 
ON {settings.INTERNAL_TABLE} USING gin (indexes);

"""
