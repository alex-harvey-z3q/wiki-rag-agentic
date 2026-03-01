from __future__ import annotations

import os


def _req(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v


AWS_REGION: str = os.getenv("AWS_REGION", "ap-southeast-2")

DB_HOST: str = _req("DB_HOST")
DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
DB_NAME: str = os.getenv("DB_NAME", "postgres")
DB_USER: str = _req("DB_USER")
DB_PASSWORD: str = _req("DB_PASSWORD")

OPENAI_API_KEY: str = _req("OPENAI_API_KEY")
EMBED_MODEL: str = os.getenv("EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")

TOP_K: int = int(os.getenv("TOP_K", "6"))
MAX_EVIDENCE_CHARS: int = int(os.getenv("MAX_EVIDENCE_CHARS", "1200"))

# Table/index names used by the indexer.
VEC_SCHEMA: str = os.getenv("VEC_SCHEMA", "public")
VEC_TABLE: str = os.getenv("VEC_TABLE", "data_wiki_rag_nodes")

# Must match the embedding model dimensionality.
# text-embedding-3-small: 1536
# text-embedding-3-large: 3072
EMBED_DIM: int = int(os.getenv("EMBED_DIM", "1536"))
