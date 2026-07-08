import re


def aggregate_markdown(raw_markdown: str) -> str:
    content = raw_markdown.strip()

    content = re.sub(r'\n{3,}', '\n\n', content)

    lines = content.split('\n')
    aggregated = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            aggregated.append(stripped)
        else:
            if aggregated and aggregated[-1] != '':
                aggregated.append('')

    result = '\n'.join(aggregated)

    return result


def inject_image_markers(markdown: str, images: list[dict]) -> str:
    if not images:
        return markdown

    marker_lines = []
    for img in images:
        marker_lines.append(f"\n[Image: {img['filename']}]")

    return markdown + "\n\n---\n" + "\n".join(marker_lines)
