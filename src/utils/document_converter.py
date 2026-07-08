from pathlib import Path


def convert_document(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".txt":
        return _convert_txt(file_path)
    elif ext == ".md":
        return _convert_md(file_path)
    elif ext == ".json":
        return _convert_json(file_path)
    elif ext == ".csv":
        return _convert_csv(file_path)
    else:
        return _convert_with_markitdown(file_path)


def _convert_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _convert_md(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _convert_json(file_path: str) -> str:
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)


def _convert_csv(file_path: str) -> str:
    import csv
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(" | ".join(row))
    return "\n".join(rows)


def _convert_with_markitdown(file_path: str) -> str:
    try:
        from markitdown import MarkItDown
        md = MarkItDown()
        result = md.convert(file_path)
        return result.text_content
    except ImportError:
        raise ImportError(
            "MarkItDown library not found. Install with: pip install markitdown"
        )
    except Exception as e:
        raise Exception(f"MarkItDown conversion failed: {str(e)}")


def get_supported_extensions() -> list[str]:
    return [".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md", ".csv", ".json", ".html", ".zip"]
