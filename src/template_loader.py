import re
import zipfile
from xml.etree import ElementTree as ET
from typing import List, Dict


def parse_template(template_path: str) -> List[Dict[str, str]]:
    """Parse a Word (.docx) template and extract form fields.

    The function scans text nodes in the document for patterns like
    ``Label: {{field_name}}`` and converts them into a structure suitable
    for generating input forms.

    Parameters
    ----------
    template_path: str
        Path to the Word template file.

    Returns
    -------
    List[Dict[str, str]]
        A list of field definitions with keys ``label``, ``name`` and ``type``.
    """
    with zipfile.ZipFile(template_path) as zf:
        xml_data = zf.read("word/document.xml")

    root = ET.fromstring(xml_data)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    fields: List[Dict[str, str]] = []
    pattern = re.compile(r"(.+?)\{\{(\w+)\}\}")

    for t in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
        if not t.text:
            continue
        match = pattern.search(t.text)
        if match:
            label, name = match.groups()
            fields.append({
                "label": label.strip().rstrip(":："),
                "name": name.strip(),
                "type": "text",
            })
    return fields

