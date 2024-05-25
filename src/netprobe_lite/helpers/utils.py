import json
from typing import Any


def get_json(text: str) -> dict[str, Any]:
    """Convert a JSON-formatted string to a dictionary object.

    Args:
        text (str): A JSON-formatted string.

    Returns:
        dict[str, Any]: A dictionary object representing the JSON data. If the input
        string is not valid JSON, an empty dictionary is returned.

    """
    try:
        json_dict = json.loads(text)
        return json_dict if isinstance(json_dict, dict) else {}
    except json.decoder.JSONDecodeError:
        return {}
