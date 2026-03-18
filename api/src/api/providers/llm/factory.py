from __future__ import annotations

from functools import lru_cache

from ... import config
from .base import LLMProvider
from .bedrock_provider import BedrockClaudeProvider
from .openai_provider import OpenAILLMProvider


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    provider = config.LLM_PROVIDER
    if provider == "bedrock":
        return BedrockClaudeProvider()
    if provider == "openai":
        return OpenAILLMProvider()
    raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider}")
