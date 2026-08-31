"""
Configuration and environment loading.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root (works regardless of CWD)
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")


def _require(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise EnvironmentError(
            f"Missing required environment variable: {key}\n"
            f"Copy .env.example → .env and fill in your keys."
        )
    return val


# ── LLM ───────────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = _require("OPENAI_API_KEY")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# ── Search ────────────────────────────────────────────────────────────────────
TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

# ── LangSmith tracing (optional) ──────────────────────────────────────────────
LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "multi-agent-web-research")

# ── Model defaults ────────────────────────────────────────────────────────────
DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o")
DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0"))
MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
