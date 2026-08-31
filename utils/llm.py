"""
LLM Factory providing unified interface across Groq, OpenAI, Anthropic, and Google Gemini.
"""
import os
from typing import Optional, Any
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
    Defaults to Groq (if GROQ_API_KEY is present) or OpenAI (if OPENAI_API_KEY is present).
    """
    # Detect provider if not specified
    if not provider:
        provider = os.getenv("LLM_PROVIDER")
        if not provider:
            if api_key and api_key.startswith("gsk_"):
                provider = "groq"
            elif os.getenv("GROQ_API_KEY"):
                provider = "groq"
            elif os.getenv("OPENAI_API_KEY"):
                provider = "openai"
            elif os.getenv("GOOGLE_API_KEY"):
                provider = "gemini"
            elif os.getenv("ANTHROPIC_API_KEY"):
                provider = "anthropic"
            else:
                provider = "groq"  # default fallback

    provider = provider.lower()

    if provider == "groq":
        try:
            from langchain_groq import ChatGroq
            groq_key = api_key or os.getenv("GROQ_API_KEY")
            selected_model = model_name or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            logger.info(f"Using Groq LLM: {selected_model}")
            return ChatGroq(
                groq_api_key=groq_key,
                model_name=selected_model,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize ChatGroq ({e}). Checking OpenAI fallback...")

    if provider == "openai" or not provider:
        try:
            from langchain_openai import ChatOpenAI
            openai_key = api_key or os.getenv("OPENAI_API_KEY")
            selected_model = model_name or os.getenv("OPENAI_MODEL", "gpt-4o")
            logger.info(f"Using OpenAI LLM: {selected_model}")
            return ChatOpenAI(
                api_key=openai_key,
                model=selected_model,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize ChatOpenAI ({e}).")

    if provider in ("google", "gemini"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            gemini_key = api_key or os.getenv("GOOGLE_API_KEY")
            selected_model = model_name or "gemini-1.5-pro"
            logger.info(f"Using Google Gemini LLM: {selected_model}")
            return ChatGoogleGenerativeAI(
                google_api_key=gemini_key,
                model=selected_model,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize ChatGoogleGenerativeAI: {e}")

    if provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
            anthropic_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            selected_model = model_name or "claude-3-5-sonnet-20241022"
            logger.info(f"Using Anthropic LLM: {selected_model}")
            return ChatAnthropic(
                api_key=anthropic_key,
                model_name=selected_model,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize ChatAnthropic: {e}")

    # Fallback to OpenAI if anything else fails
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY", "dummy"),
        model=model_name or "gpt-4o",
        temperature=temperature,
    )
