import os

PARSED_BUCKET = os.environ["PARSED_BUCKET"]
PARSED_PREFIX = os.environ.get("PARSED_PREFIX", "docs/")

AWS_REGION = os.environ.get("AWS_REGION", "ap-southeast-2")
AWS_PROFILE = os.environ.get("AWS_PROFILE")

EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "openai").strip().lower()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_EMBED_MODEL = os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-small")

BEDROCK_EMBED_MODEL_ID = os.environ.get(
    "BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-g1-text-02"
)

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

PGVECTOR_TABLE = os.environ.get("PGVECTOR_TABLE", "wiki_rag_nodes")
PGVECTOR_SCHEMA = os.environ.get("PGVECTOR_SCHEMA", "public")
EMBED_DIM = int(os.environ.get("EMBED_DIM", "1536"))
