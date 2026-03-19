from __future__ import annotations

from indexer import settings


def get_embedding_model():
    provider = settings.EMBEDDING_PROVIDER

    if provider != "bedrock":
        raise RuntimeError(
            f"Unsupported EMBEDDING_PROVIDER for Bedrock-only indexer: {provider}"
        )

    from llama_index.embeddings.bedrock import BedrockEmbedding

    kwargs: dict = {
        "model_name": settings.BEDROCK_EMBED_MODEL_ID,
        "region_name": settings.AWS_REGION,
    }

    if settings.AWS_PROFILE:
        kwargs["profile_name"] = settings.AWS_PROFILE

    return BedrockEmbedding(**kwargs)
