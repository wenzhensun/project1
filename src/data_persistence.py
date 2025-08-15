import json
from pathlib import Path
from typing import Dict, List


def load_previous_data(path: str) -> Dict[str, str]:
    """Load previous data from a JSON file."""
    data_path = Path(path)
    if not data_path.exists():
        return {}
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def autofill_fields(fields: List[Dict[str, str]], data: Dict[str, str]) -> List[Dict[str, str]]:
    """Populate ``value`` for fields using the provided data."""
    filled = []
    for field in fields:
        value = data.get(field["name"])
        new_field = dict(field)
        if value is not None:
            new_field["value"] = value
        filled.append(new_field)
    return filled

