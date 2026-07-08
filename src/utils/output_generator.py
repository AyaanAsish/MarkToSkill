import os
import re
from datetime import datetime


def generate_skill_file(content: str, output_path: str) -> str:
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    sanitized = _sanitize_output(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sanitized)

    return output_path


def _sanitize_output(content: str) -> str:
    content = re.sub(r'^```\w*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```$', '', content, flags=re.MULTILINE)

    content = content.strip()

    return content


def add_metadata_header(content: str, source_file: str = "") -> str:
    now = datetime.now().isoformat()
    header = f"""---
title: Generated Skill Document
source: {source_file}
generated_at: {now}
---

"""
    return header + content
