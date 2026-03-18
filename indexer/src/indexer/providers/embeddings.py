from __future__ import annotations

from indexer import settings


def get_embedding_model():
    provider = settings.EMBEDDING_PROVIDER

    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai")
        from llama_index.embeddings.openai import OpenAIEmbedding

        return OpenAIEmbedding(
            model=settings.OPENAI_EMBED_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    if provider == "bedrock":
        from llama_index.embeddings.bedrock import BedrockEmbedding

        kwargs: dict = {
            "model_name": settings.BEDROCK_EMBED_MODEL_ID,
            "region_name": settings.AWS_REGION,
        }
        if settings.AWS_PROFILE:
            kwargs["profile_name"] = settings.AWS_PROFILE
        return BedrockEmbedding(**kwargs)

    raise RuntimeError(f"Unsupported EMBEDDING_PROVIDER: {provider}")
