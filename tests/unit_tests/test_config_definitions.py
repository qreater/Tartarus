import pytest
from app.utils.config_definitions import validations


def test_validate_json_schema():
    """
    Test that the validate_json_schema function correctly validates a JSON schema.

    This test verifies that the function correctly validates a JSON schema
    against the JSON schema specification. It tests a valid schema and an
    invalid schema to ensure that the function returns the correct result.
    """
    valid_schema = {"type": "object", "properties": {"test_key": {"type": "string"}}}

    invalid_schema = {
        "type": "object",
        "properties": {"test_key": {"type": "string"}, "new_key": {"type": "string"}},
    }

    assert validations.validate_json_schema(valid_schema) is True
    assert validations.validate_json_schema(invalid_schema) is False


def test_validate_primary_key():
    """
    Test that the validate_primary_key function correctly validates a primary key.

    This test verifies that the function correctly validates a primary key
    against the JSON schema specification. It tests a valid primary key and an
    invalid primary key to ensure that the function returns the correct result.
    """
    valid_primary_key = "test_key"
    invalid_primary_key = "new_key"

    assert validations.validate_primary_key(valid_primary_key) is True
    assert validations.validate_primary_key(invalid_primary_key) is False


def test_validate_secondary_indexes():
    """
    Test that the validate_secondary_indexes function correctly validates secondary indexes.

    This test verifies that the function correctly validates secondary indexes
    against the JSON schema specification. It tests valid secondary indexes and
    invalid secondary indexes to ensure that the function returns the correct result.
    """
    valid_secondary_indexes = ["test_key"]
    invalid_secondary_indexes = ["new_key"]

    assert validations.validate_secondary_indexes(valid_secondary_indexes) is True
    assert validations.validate_secondary_indexes(invalid_secondary_indexes) is False
