from ollama import Client
from src.core.config import OLLAMA_HOST, OLLAMA_MODEL

SYSTEM_PROMPT = """
You are a skill-documentation generator.

Your task is to analyze provided markdown content and generate a well-structured skill.md file.
The skill.md should be a self-contained instructional document that teaches the user how to
perform a specific task or skill based on the source material.

Output Format:
- Use proper markdown headings (#, ##, ###)
- Include a clear title and description at the top
- Break down the skill into logical steps or sections
- Include code examples where relevant
- Add a "References" or "See Also" section at the end if applicable
- Keep the output concise and actionable

Do not include explanations about your process. Only output the skill.md content.
There is also no need to include long sections of code snippets, well explained instruction set is good.

Note: The source content is capped at 12,000 characters and may be truncated. Cover the most important information from what you receive; if truncated, prioritize covering the beginning of the document where key context typically lives.
"""


MAX_INPUT_CHARS = 12000
MAX_OUTPUT_TOKENS = 32768
MAX_CONTEXT_TOKENS = 65536


def query_llm(content: str, user_prompt: str = "", model: str = None, host: str = None) -> str:
    truncated = content[:MAX_INPUT_CHARS]
    if len(content) > MAX_INPUT_CHARS:
        truncated += "\n\n[Content truncated — only showing first {:,} characters]".format(MAX_INPUT_CHARS)

    prompt = f"""
Source Content:
{truncated}

User Instructions:
{user_prompt}

Generate a complete skill.md document from this content. Cover all key points thoroughly.
Do not stop until the document is fully complete.
"""

    ollama_host = host or OLLAMA_HOST
    ollama_model = model or OLLAMA_MODEL

    client = Client(host=ollama_host)

    response = client.chat(
        model=ollama_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        options={
            "num_predict": MAX_OUTPUT_TOKENS,
            "num_ctx": MAX_CONTEXT_TOKENS,
        },
    )

    return response["message"]["content"]


def check_ollama_connection(host: str = None) -> dict:
    ollama_host = host or OLLAMA_HOST

    try:
        client = Client(host=ollama_host)
        models = client.list()

        model_names = []
        for m in models.get("models", []):
            model_id = m.get("name") or m.get("model") or m.get("id")
            if model_id:
                model_names.append(model_id)

        configured_model = OLLAMA_MODEL
        model_available = (
            configured_model in model_names or
            any(configured_model in name for name in model_names)
        )

        return {
            "connected": True,
            "host": ollama_host,
            "models": model_names,
            "configured_model": configured_model,
            "model_available": model_available,
        }
    except Exception as e:
        return {
            "connected": False,
            "host": ollama_host,
            "error": str(e),
            "models": [],
            "configured_model": OLLAMA_MODEL,
            "model_available": False,
        }
