"""
LLM Factory providing unified interface across Groq, OpenAI, Anthropic, and Google Gemini.
"""
import os
from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from loguru import logger


def get_llm(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.2,
    api_key: Optional[str] = None,
) -> BaseChatModel:
    """
    Get configured ChatModel instance.
    Supports Groq, OpenAI, Google Gemini, and Anthropic.
    Raises clear error if no valid key is provided.
    """
    # Auto-detect provider if not explicitly given
    if not provider:
        if api_key and api_key.startswith("gsk_"):
            provider = "groq"
        elif api_key and api_key.startswith("sk-ant-"):
            provider = "anthropic"
        elif api_key and (api_key.startswith("sk-") or api_key.startswith("sess-")):
            provider = "openai"
        elif os.getenv("GROQ_API_KEY"):
            provider = "groq"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("GOOGLE_API_KEY"):
            provider = "gemini"
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
        else:
            provider = "groq"

    provider = provider.lower()

    # 1. Groq Cloud
    if provider == "groq":
        groq_key = api_key or os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key.startswith("gsk_..."):
            raise ValueError(
                "Missing Groq API Key! Please set GROQ_API_KEY in .env or enter your key in the UI Settings modal (Get a free key at https://console.groq.com)."
            )
        from langchain_groq import ChatGroq
        selected_model = model_name or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        logger.info(f"Using Groq LLM: {selected_model}")
        return ChatGroq(
            groq_api_key=groq_key,
            model_name=selected_model,
            temperature=temperature,
        )

    # 2. OpenAI
    if provider == "openai":
        openai_key = api_key or os.getenv("OPENAI_API_KEY")
        if not openai_key or openai_key.startswith("sk-..."):
            raise ValueError(
                "Missing OpenAI API Key! Please set OPENAI_API_KEY in .env or enter your key in the UI Settings modal (https://platform.openai.com)."
            )
        from langchain_openai import ChatOpenAI
        selected_model = model_name or os.getenv("OPENAI_MODEL", "gpt-4o")
        logger.info(f"Using OpenAI LLM: {selected_model}")
        return ChatOpenAI(
            api_key=openai_key,
            model=selected_model,
            temperature=temperature,
        )

    # 3. Google Gemini
    if provider in ("google", "gemini"):
        gemini_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not gemini_key or gemini_key.startswith("AIza..."):
            raise ValueError(
                "Missing Google API Key! Please set GOOGLE_API_KEY in .env or enter your key in the UI Settings modal (https://aistudio.google.com)."
            )
        from langchain_google_genai import ChatGoogleGenerativeAI
        selected_model = model_name or "gemini-1.5-pro"
        logger.info(f"Using Google Gemini LLM: {selected_model}")
        return ChatGoogleGenerativeAI(
            google_api_key=gemini_key,
            model=selected_model,
            temperature=temperature,
        )

    # 4. Anthropic
    if provider == "anthropic":
        anthropic_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_key or anthropic_key.startswith("sk-ant-..."):
            raise ValueError(
                "Missing Anthropic API Key! Please set ANTHROPIC_API_KEY in .env or enter your key in the UI Settings modal (https://console.anthropic.com)."
            )
        from langchain_anthropic import ChatAnthropic
        selected_model = model_name or "claude-3-5-sonnet-20241022"
        logger.info(f"Using Anthropic LLM: {selected_model}")
        return ChatAnthropic(
            api_key=anthropic_key,
            model_name=selected_model,
            temperature=temperature,
        )

    raise ValueError(f"Unsupported LLM provider: '{provider}'. Supported: groq, openai, gemini, anthropic.")
