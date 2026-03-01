import os

PARSED_BUCKET = os.environ["PARSED_BUCKET"]
PARSED_PREFIX = os.environ.get("PARSED_PREFIX", "docs/")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

PGVECTOR_TABLE = os.environ.get("PGVECTOR_TABLE", "wiki_rag_nodes")
PGVECTOR_SCHEMA = os.environ.get("PGVECTOR_SCHEMA", "public")
