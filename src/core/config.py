import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")

API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
UI_PORT: int = int(os.getenv("UI_PORT", "3000"))

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

PROJECT_ROOT = Path(__file__).parent.parent.parent
TMP_INPUT_PATH: str = os.getenv("TMP_INPUT_PATH", str(PROJECT_ROOT / "tmp" / "input"))
TMP_OUTPUT_PATH: str = os.getenv("TMP_OUTPUT_PATH", str(PROJECT_ROOT / "tmp" / "output"))
TMP_ASSETS_PATH: str = os.getenv("TMP_ASSETS_PATH", str(PROJECT_ROOT / "tmp" / "assets"))


def validate_config() -> dict[str, bool]:
    return {
        "ollama_host": bool(OLLAMA_HOST),
        "ollama_model": bool(OLLAMA_MODEL),
    }


def get_config_summary() -> dict:
    return {
        "ollama": {
            "host": OLLAMA_HOST,
            "model": OLLAMA_MODEL,
        },
        "server": {
            "api_host": API_HOST,
            "api_port": API_PORT,
            "ui_port": UI_PORT,
        },
        "logging": {
            "level": LOG_LEVEL,
        },
    }
