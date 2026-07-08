import os
from typing import Any, Dict
from src.utils.document_converter import convert_document
from src.utils.image_extractor import extract_images_from_doc
from src.utils.markdown_aggregator import aggregate_markdown, inject_image_markers
from src.utils.output_generator import generate_skill_file
from src.clients.llm import query_llm
from src.core.config import TMP_OUTPUT_PATH, TMP_ASSETS_PATH


def process_document_tool(file_path: str) -> Dict[str, Any]:
    try:
        markdown_content = convert_document(file_path)
        return {
            "status": "success",
            "markdown": markdown_content,
            "file_path": file_path,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "markdown": "",
        }


def extract_images_tool(file_path: str) -> Dict[str, Any]:
    try:
        images = extract_images_from_doc(file_path, TMP_ASSETS_PATH)
        return {
            "status": "success",
            "images": images,
            "image_count": len(images),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "images": [],
        }


def run_agent(file_paths: list[str], user_prompt: str) -> str:
    os.makedirs(TMP_OUTPUT_PATH, exist_ok=True)
    os.makedirs(TMP_ASSETS_PATH, exist_ok=True)

    output_path = os.path.join(TMP_OUTPUT_PATH, "skill.md")

    if isinstance(file_paths, str):
        file_paths = [file_paths]

    print(f" Starting MarkToSkill Agent Workflow...")
    print(f"   Input files ({len(file_paths)}):")
    for fp in file_paths:
        print(f"     - {fp}")
    print(f"   Instructions: {user_prompt}")
    print(f"   Output: {output_path}")
    print()

    try:
        all_markdown = []
        all_images = []
        failures = []

        for i, file_path in enumerate(file_paths):
            print(f"   [{i + 1}/{len(file_paths)}] Processing: {os.path.basename(file_path)}")

            print("      Converting document to markdown...")
            result = process_document_tool(file_path)
            if result["status"] != "success":
                err_msg = result.get('error', 'Unknown error')
                print(f"      ⚠ Conversion failed: {err_msg}")
                failures.append(f"{os.path.basename(file_path)}: {err_msg}")
                continue
            markdown_content = result["markdown"]
            all_markdown.append(markdown_content)
            print(f"      ✓ Extracted markdown ({len(markdown_content)} chars)")

            print("      Extracting images...")
            image_result = extract_images_tool(file_path)
            if image_result["status"] == "success" and image_result["image_count"] > 0:
                all_images.extend(image_result["images"])
                print(f"      ✓ Extracted {image_result['image_count']} images")
            else:
                print("      - No images extracted")

        if not all_markdown:
            detail = "; ".join(failures) if failures else "All files failed with unknown errors"
            raise Exception(f"No documents could be processed successfully: {detail}")

        combined_markdown = "\n\n---\n\n".join(all_markdown)

        print(f"\n   3. Aggregating and normalizing content ({len(combined_markdown)} total chars)...")
        aggregated = aggregate_markdown(combined_markdown)
        print(f"   ✓ Aggregated content ({len(aggregated)} chars)")

        if all_images:
            aggregated = inject_image_markers(aggregated, all_images)
            print(f"   ✓ Injected {len(all_images)} image markers")

        print("   4. Generating skill document with LLM...")
        llm_output = query_llm(aggregated, user_prompt)
        print(f"   ✓ LLM response received ({len(llm_output)} chars)")

        print("   5. Writing skill.md file...")
        generate_skill_file(llm_output, output_path)
        print(f"   ✓ Generated: {output_path}")

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"\n✓ Workflow complete!")
            print(f"   Output: {output_path} ({file_size:,} bytes)")
        else:
            print(f"\n⚠ Workflow completed but output file not found")

        return output_path

    except Exception as e:
        print(f"\n✗ Workflow failed: {str(e)}")
        raise
