import json
import re
import uuid


def is_valid_uuid(uuid_str):
    """
    Checks if the given string is a valid UUID.

    Args:
        uuid_str: The string to be checked.

    Returns:
        True if the string is a valid UUID, False otherwise.
    """
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False
