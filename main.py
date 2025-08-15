from src.template_loader import parse_template
from src.data_persistence import load_previous_data, autofill_fields
from typing import List, Dict
import json

def generate_form(template_path: str, data_path: str) -> List[Dict[str, str]]:
    fields = parse_template(template_path)
    data = load_previous_data(data_path)
    return autofill_fields(fields, data)


def main(template_path: str, data_path: str) -> None:
    filled = generate_form(template_path, data_path)
    print(json.dumps(filled, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <template.docx> <data.json>")
    else:
        main(sys.argv[1], sys.argv[2])
