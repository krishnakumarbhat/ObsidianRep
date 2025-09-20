"""
Utility functions for the Flask application.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict


def serialize_for_json(obj: Any) -> Dict[str, Any]:
    """
    Convert objects to JSON-serializable format.
    Handles enums, datetime objects, and other non-serializable types.
    """
    if isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        # Handle dataclass objects
        result = {}
        for key, value in obj.__dict__.items():
            result[key] = serialize_for_json(value)
        return result
    else:
        return obj


def prepare_response_data(data: Any) -> Dict[str, Any]:
    """
    Prepare data for JSON response.
    """
    if isinstance(data, list):
        return [serialize_for_json(item) for item in data]
    else:
        return serialize_for_json(data)