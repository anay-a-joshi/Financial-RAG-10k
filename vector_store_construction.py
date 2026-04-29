"""
vector_store_construction.py

Chunk processed 10-K filings and load them into a persistent ChromaDB
vector store with embeddings from a local Hugging Face model.

For every {ticker}_{year}/content.txt under PROCESSED_DATA_DIR:
  - Read the cleaned text.
  - Split it into chunks with SentenceSplitter (paragraph- and sentence-
    aware, 1024-token chunks with 100-token overlap).
  - Wrap each chunk in a TextNode tagged with metadata:
        ticker, year, filing_id, chunk_index
  - Embed and write all nodes to a single ChromaDB collection
    "financial_filings" inside VECTOR_STORE_DIR.

The same embedding model used here MUST be reused at query time
(see system.py); cosine similarity only makes sense in a shared space.

Author: Anay Abhijit Joshi
Student ID: 904168649
"""

import os
import shutil

import chromadb

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from config import (
    PROCESSED_DATA_DIR,
    VECTOR_STORE_DIR,
    EMBED_MODEL_NAME,
)


COLLECTION_NAME: str = "financial_filings"

# Chunking parameters tuned for 10-K filings: large enough to keep
# section context, small enough that retrieval stays precise. The 100-
# token overlap helps when an answer straddles a chunk boundary.
CHUNK_SIZE: int = 1024
CHUNK_OVERLAP: int = 100

# Paragraph- and sentence-aware separators so chunks break on natural
# boundaries instead of mid-sentence.
PARAGRAPH_SEPARATOR: str = "\n\n"
SECONDARY_CHUNKING_REGEX: str = r"[^,.;。？！]+[,.;。？！]?"


# A single splitter reused for every filing.
splitter = SentenceSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    paragraph_separator=PARAGRAPH_SEPARATOR,
    secondary_chunking_regex=SECONDARY_CHUNKING_REGEX,
)

# Embedding model. Downloaded on first run, cached locally afterwards.
print(f"Loading embedding model: {EMBED_MODEL_NAME}")
embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)


def parse_dir_name(name: str) -> tuple[str, str] | None:
    """Parse '{ticker}_{year}' into (ticker, year). Return None if invalid."""
    if "_" not in name:
        return None
    ticker, _, year = name.rpartition("_")
    if not ticker or not year.isdigit() or len(year) != 4:
        return None
    return ticker, year


def get_file_chunks(file_dir: str) -> list[str]:
    """Read content.txt and return a list of chunk strings."""
    content_path = os.path.join(file_dir, "content.txt")
    if not os.path.isfile(content_path):
        return []
    with open(content_path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text.strip():
        return []
    return splitter.split_text(text)


def get_all_nodes(filings_dir: str) -> list[TextNode]:
    """
    Walk every {ticker}_{year} directory, chunk its content.txt, and
    produce TextNode objects with retrieval metadata attached.
    """
    if not os.path.isdir(filings_dir):
        raise FileNotFoundError(
            f"{filings_dir} not found. Run data_processing.py first."
        )

    all_nodes: list[TextNode] = []
    per_filing_counts: list[tuple[str, str, int]] = []

    for entry in sorted(os.listdir(filings_dir)):
        full_path = os.path.join(filings_dir, entry)
        if not os.path.isdir(full_path):
            continue
        parsed = parse_dir_name(entry)
        if parsed is None:
            print(f"  [skip] {entry}: not in {{ticker}}_{{year}} format")
            continue
        ticker, year = parsed

        chunks = get_file_chunks(full_path)
        if not chunks:
            print(f"  [warn] {entry}: empty or missing content.txt")
            continue

        filing_id = f"{ticker}_{year}"
        for i, chunk_text in enumerate(chunks):
            node = TextNode(
                text=chunk_text,
                metadata={
                    "ticker": ticker,
                    "year": year,
                    "filing_id": filing_id,
                    "chunk_index": i,
                },
                # Stable per-chunk id helps with deduplication on re-runs.
                id_=f"{filing_id}__{i}",
            )
            # Keep all metadata fields visible to the embedding model
            # disabled so the embedding represents text content only,
            # while still being filterable at retrieval time.
            node.excluded_embed_metadata_keys = [
                "ticker", "year", "filing_id", "chunk_index"
            ]
            node.excluded_llm_metadata_keys = ["chunk_index"]
            all_nodes.append(node)

        per_filing_counts.append((ticker, year, len(chunks)))
        print(f"  {filing_id}: {len(chunks)} chunks")

    # Summary
    print("\n" + "=" * 50)
    print(f"Filings processed: {len(per_filing_counts)}")
    print(f"Total chunks:      {len(all_nodes)}")
    return all_nodes


def build_vector_store(all_nodes: list[TextNode]) -> None:
    """Build a fresh persistent ChromaDB and index all nodes into it."""
    if not all_nodes:
        raise RuntimeError("No nodes to index. Aborting.")

    # Wipe any prior store so re-runs are deterministic.
    if os.path.isdir(VECTOR_STORE_DIR):
        print(f"\nRemoving existing vector store at {VECTOR_STORE_DIR}")
        shutil.rmtree(VECTOR_STORE_DIR)
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    print(f"Initializing ChromaDB at {VECTOR_STORE_DIR}")
    client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print(f"Embedding and indexing {len(all_nodes)} chunks...")
    print("(First run will download the embedding model -- be patient.)\n")

    VectorStoreIndex(
        all_nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
    )

    print(f"\nDone. Vector store written to {VECTOR_STORE_DIR}")
    print(f"Collection: '{COLLECTION_NAME}'")
    print(f"Documents:  {collection.count()}")


def main() -> None:
    print(f"Reading filings from {PROCESSED_DATA_DIR}\n")
    all_nodes = get_all_nodes(PROCESSED_DATA_DIR)
    build_vector_store(all_nodes)


if __name__ == "__main__":
    main()