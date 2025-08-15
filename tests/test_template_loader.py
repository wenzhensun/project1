import sys, os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import zipfile
from pathlib import Path

from src.template_loader import parse_template
from main import generate_form


def create_docx(path: Path) -> None:
    files = {
        "[Content_Types].xml": (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
            "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
            "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
            "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
            "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>"
            "<Override PartName=\"/word/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/>"
            "</Types>"
        ),
        "_rels/.rels": (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
            "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
            "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>"
            "</Relationships>"
        ),
        "word/_rels/document.xml.rels": (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
            "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"></Relationships>"
        ),
        "word/styles.xml": (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
            "<w:styles xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"></w:styles>"
        ),
        "word/document.xml": (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
            "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">"
            "<w:body>"
            "<w:p><w:r><w:t>Name: {{name}}</w:t></w:r></w:p>"
            "<w:p><w:r><w:t>Age: {{age}}</w:t></w:r></w:p>"
            "</w:body></w:document>"
        ),
    }
    with zipfile.ZipFile(path, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)


def test_parse_template(tmp_path: Path):
    docx_path = tmp_path / "template.docx"
    create_docx(docx_path)
    fields = parse_template(str(docx_path))
    assert fields == [
        {"label": "Name", "name": "name", "type": "text"},
        {"label": "Age", "name": "age", "type": "text"},
    ]


def test_generate_form_autofill(tmp_path: Path):
    docx_path = tmp_path / "template.docx"
    create_docx(docx_path)
    data_path = tmp_path / "data.json"
    data_path.write_text(json.dumps({"name": "Alice", "age": "30"}), encoding="utf-8")
    result = generate_form(str(docx_path), str(data_path))
    assert any(f["name"] == "name" and f.get("value") == "Alice" for f in result)
    assert any(f["name"] == "age" and f.get("value") == "30" for f in result)
