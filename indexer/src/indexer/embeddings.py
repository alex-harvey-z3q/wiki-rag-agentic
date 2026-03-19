from __future__ import annotations

from llama_index.core import Settings

from indexer.providers import get_embedding_model


def configure_embeddings():
    embed_model = get_embedding_model()
    Settings.embed_model = embed_model
    return embed_model


def embed(text: str):
    model = configure_embeddings()
    return model.get_text_embedding(text)
