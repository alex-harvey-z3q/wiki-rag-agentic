from __future__ import annotations

from functools import lru_cache

from ... import config


@lru_cache(maxsize=1)
def get_embedding_model():
    provider = config.EMBEDDING_PROVIDER

    if provider == "openai":
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai")
        from llama_index.embeddings.openai import OpenAIEmbedding

        return OpenAIEmbedding(
            model=config.OPENAI_EMBED_MODEL,
            api_key=config.OPENAI_API_KEY,
        )

    if provider == "bedrock":
        from llama_index.embeddings.bedrock import BedrockEmbedding

        kwargs: dict = {
            "model_name": config.BEDROCK_EMBED_MODEL_ID,
            "region_name": config.AWS_REGION,
        }
        if config.AWS_PROFILE:
            kwargs["profile_name"] = config.AWS_PROFILE
        return BedrockEmbedding(**kwargs)

    raise RuntimeError(f"Unsupported EMBEDDING_PROVIDER: {provider}")
