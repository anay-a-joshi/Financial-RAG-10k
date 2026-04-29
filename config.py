import os

ROOT_DIR: str = "."

DATA_DIR: str = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
ORIGINAL_DATA_DIR: str = os.path.join(DATA_DIR, "original")
os.makedirs(ORIGINAL_DATA_DIR, exist_ok=True)
PROCESSED_DATA_DIR: str = os.path.join(DATA_DIR, "processed")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
VECTOR_STORE_DIR: str = os.path.join(DATA_DIR, "vector_store")
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Recommended lightweight local embedding model.
EMBED_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"

# Recommended lightweight local LLM via Ollama.
# Reasonable alternatives include:
#   - "qwen2.5:3b"
#   - "phi4-mini:3.8b"
LLM_MODEL_NAME: str = "llama3.2:3b"
LLM_BACKEND: str = "ollama"  # one of: "ollama", "huggingface"
