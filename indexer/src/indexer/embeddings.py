from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from indexer.settings import OPENAI_API_KEY, EMBED_MODEL

def configure_embeddings():
    Settings.embed_model = OpenAIEmbedding(
        model=EMBED_MODEL,
        api_key=OPENAI_API_KEY,
    )
