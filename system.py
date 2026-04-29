"""
system.py

End-to-end Retrieval-Augmented Generation (RAG) pipeline over the
ChromaDB vector store of cleaned 10-K filings.

The RAGSystem class:
  - Loads the same Hugging Face embedding model used at index time.
  - Connects to the persistent ChromaDB collection.
  - Builds a retriever with metadata filtering on (ticker, year).
  - Generates answers with a local LLM via Ollama (or HuggingFaceLLM).
  - Returns both the generated answer and the most relevant chunk.

The bottom of this file runs a manual evaluation: 2 questions per
ticker (across two different fiscal years to demonstrate metadata
filtering), results written to evaluation_results.md.

Author: Anay Abhijit Joshi
Student ID: 904168649
"""

import os
import time
from typing import Optional

import chromadb

from llama_index.core import (
    PromptTemplate,
    QueryBundle,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import (
    ExactMatchFilter,
    MetadataFilters,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

from config import (
    VECTOR_STORE_DIR,
    EMBED_MODEL_NAME,
    LLM_MODEL_NAME,
    LLM_BACKEND,
)


COLLECTION_NAME: str = "financial_filings"

# Top-k chunks retrieved per query. Increased from 5 to 8 to expand
# the LLM's context window so questions whose answer lives in the
# 6th-8th most similar chunk are still answerable.
RETRIEVER_SIMILARITY_TOP_K: int = 8

# Prompt template. Tells the LLM to stay grounded in the retrieved
# context and decline only when the answer is genuinely absent.
# The numbered rules and explicit refusal sentence prevent the small
# local LLM from inventing facts; the "genuinely" wording prevents
# over-refusal when the answer is present but spread across chunks.
QA_PROMPT_TEMPLATE = PromptTemplate(
    """\
You are a financial-analysis assistant answering questions about a
company's 10-K filing. Follow these rules:

RULES:
1. Use ONLY information that appears in the "Context" section below.
2. Do NOT use outside knowledge, even if you know the answer.
3. If the answer is genuinely not present in the context (for example,
   the question is about an unrelated topic such as the population of
   a country), reply with this sentence:
       The information is not available in the provided filing.
   Do NOT refuse just because the answer is partial or scattered across
   multiple chunks; synthesize what is present.
4. Do NOT invent or guess numbers, names, dates, or facts.
5. Do NOT pull a number from the context just because it looks like a
   numeric answer; the number must specifically address the question.
6. Be concise but specific: name segments, products, brands, and figures
   when they appear in the context.

Ticker: {ticker}
Fiscal Year: {year}

Context:
---
{context}
---

Question: {query}

Answer (concise, factual, grounded in the context above):"""
)


class RAGSystem:
    def __init__(self, use_reranker: bool = False):
        # Embedding model: same one used at index time.
        self._embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)

        # Connect to the persistent ChromaDB collection.
        client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
        collection = client.get_or_create_collection(COLLECTION_NAME)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        self._index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
            embed_model=self._embed_model,
        )

        # LLM: Ollama by default (fast local inference), HF as alternative.
        # temperature=0.0 maximizes adherence to the prompt's refusal rule.
        # request_timeout=300 gives generation enough headroom for the
        # occasional long answer (some financial-table-heavy contexts can
        # take >3 minutes on a 3B-param local model).
        if LLM_BACKEND == "ollama":
            self._llm = Ollama(
                model=LLM_MODEL_NAME,
                request_timeout=300.0,
                temperature=0.0,
            )
        elif LLM_BACKEND == "huggingface":
            self._llm = HuggingFaceLLM(model_name=LLM_MODEL_NAME)
        else:
            raise ValueError(f"Unsupported LLM_BACKEND: {LLM_BACKEND}")

        # Optional reranker (disabled by default; flag exists for the
        # report's "what we tried" section).
        self._reranker = None
        if use_reranker:
            from llama_index.postprocessor.flag_embedding_reranker import (
                FlagEmbeddingReranker,
            )
            self._reranker = FlagEmbeddingReranker(
                model="BAAI/bge-reranker-base", top_n=3
            )

    def get_available_filings(self) -> list[tuple[str, str]]:
        """
        Return all (ticker, year) pairs present in the vector store.
        Useful for populating the Streamlit dropdowns.
        """
        client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
        collection = client.get_or_create_collection(COLLECTION_NAME)
        # Pull metadata for every doc; cheap because chunks are small.
        result = collection.get(include=["metadatas"])
        seen: set[tuple[str, str]] = set()
        for md in result.get("metadatas") or []:
            t = md.get("ticker")
            y = md.get("year")
            if t and y:
                seen.add((t, y))
        return sorted(seen)

    def respond(
        self,
        query: str,
        ticker: str,
        year: str,
    ) -> tuple[str, Optional[TextNode], list[TextNode]]:
        """
        Run the full retrieval + generation pipeline.

        Returns:
            (answer_text, best_node, all_retrieved_nodes)

        best_node may be None if nothing matches the metadata filter.
        """
        if not query or not query.strip():
            return ("Please enter a question.", None, [])

        query_bundle = QueryBundle(query.strip())

        # Metadata filters: ticker AND year must match exactly.
        filters = MetadataFilters(
            filters=[
                ExactMatchFilter(key="ticker", value=ticker),
                ExactMatchFilter(key="year", value=str(year)),
            ]
        )

        retriever = self._index.as_retriever(
            similarity_top_k=RETRIEVER_SIMILARITY_TOP_K,
            filters=filters,
        )

        retrieved = retriever.retrieve(query_bundle)
        if not retrieved:
            return (
                f"No filing found for {ticker} in fiscal year {year}.",
                None,
                [],
            )

        # Optional rerank on top-k.
        if self._reranker is not None:
            retrieved = self._reranker.postprocess_nodes(
                retrieved, query_bundle=query_bundle
            )

        nodes = [r.node for r in retrieved]
        best_node = nodes[0]

        context_str = "\n\n---\n\n".join(n.get_content() for n in nodes)
        prompt = QA_PROMPT_TEMPLATE.format(
            ticker=ticker,
            year=str(year),
            context=context_str,
            query=query,
        )
        response = self._llm.complete(prompt)

        return str(response).strip(), best_node, nodes


# ---------------------------------------------------------------------------
# Manual evaluation: 2 test questions per ticker -> markdown report.
# ---------------------------------------------------------------------------

# Two diverse questions per ticker designed to exercise different
# parts of a 10-K (business overview, financial figures, risks, etc.).
EVALUATION_QUESTIONS: dict[str, list[str]] = {
    "AFL": [
        "What are Aflac's primary insurance product lines and in which "
        "geographic markets does the company operate?",
        "What were the principal risk factors disclosed by Aflac, and how "
        "does foreign currency exposure affect its results?",
    ],
    "CAT": [
        "What are Caterpillar's main reporting segments and what products "
        "or services does each segment provide?",
        "How does Caterpillar describe the seasonality and cyclical nature "
        "of demand for its construction and mining equipment?",
    ],
    "IBM": [
        "What are IBM's main business segments and which segment "
        "contributes the largest share of revenue?",
        "What does IBM disclose about its research and development "
        "spending and its strategic focus areas?",
    ],
    "KMB": [
        "What are Kimberly-Clark's main product categories and which "
        "consumer brands does it own?",
        "How does Kimberly-Clark describe the impact of raw material "
        "costs (e.g. pulp) on its margins?",
    ],
    "KR": [
        "How many stores does Kroger operate and what banners or formats "
        "does it use?",
        "What does Kroger disclose about competition in the grocery "
        "retail industry?",
    ],
    "MS": [
        "What are Morgan Stanley's main business segments and the types "
        "of clients each serves?",
        "What does Morgan Stanley disclose about regulatory capital "
        "requirements and its capital ratios?",
    ],
    "NVDA": [
        "What are NVIDIA's main product platforms and target markets?",
        "What does NVIDIA say about competition in the GPU and "
        "data-center markets?",
    ],
    "PNC": [
        "What are PNC's main banking business segments and the types of "
        "products each offers?",
        "What does PNC disclose about credit risk and its allowance for "
        "loan and lease losses?",
    ],
    "PSA": [
        "Where are Public Storage's properties located and how many "
        "facilities does it operate?",
        "What does Public Storage disclose about its primary sources of "
        "revenue and occupancy rates?",
    ],
    "TECH": [
        "What products does Bio-Techne (TECH) sell and which scientific "
        "markets does it serve?",
        "What does the company disclose about its acquisition strategy "
        "and recent acquisitions?",
    ],
}

# Per ticker, pick two different years to demonstrate metadata filtering
# works across the full year range, not just one snapshot.
EVAL_YEAR_BY_TICKER_Q1: dict[str, str] = {
    "AFL": "2018", "CAT": "2018", "IBM": "2018", "KMB": "2018",
    "KR": "2018", "MS": "2018", "NVDA": "2018", "PNC": "2018",
    "PSA": "2018", "TECH": "2018",
}
EVAL_YEAR_BY_TICKER_Q2: dict[str, str] = {
    "AFL": "2015", "CAT": "2015", "IBM": "2015", "KMB": "2015",
    "KR": "2015", "MS": "2015", "NVDA": "2015", "PNC": "2015",
    "PSA": "2015", "TECH": "2015",
}

EVAL_OUTPUT_FILE: str = "evaluation_results.md"


def run_evaluation() -> None:
    """Run 2 questions per ticker and write a Markdown report."""
    print("Initializing RAG system for evaluation...")
    rag = RAGSystem(use_reranker=False)

    # Sanity check: which filings are actually available?
    available = set(rag.get_available_filings())
    print(f"  Found {len(available)} (ticker, year) filings in the store.\n")

    lines: list[str] = []
    lines.append("# RAG Evaluation Results\n")
    lines.append(
        f"**Student:** Anay Abhijit Joshi  \n"
        f"**Student ID:** 904168649  \n"
        f"**Embedding model:** `{EMBED_MODEL_NAME}`  \n"
        f"**LLM:** `{LLM_MODEL_NAME}` via {LLM_BACKEND}  \n"
        f"**Top-k retrieved per query:** {RETRIEVER_SIMILARITY_TOP_K}\n"
    )
    lines.append(
        "Each ticker has 2 manual test questions, run against two different "
        "fiscal years (2018 and 2015) to demonstrate that metadata filtering "
        "works across the full year range. For each question we show the "
        "question, the **highest-ranked retrieved chunk** (truncated), and "
        "the **generated answer**.\n"
    )

    total = sum(len(qs) for qs in EVALUATION_QUESTIONS.values())
    asked = 0
    t0 = time.time()

    for ticker in sorted(EVALUATION_QUESTIONS):
        lines.append(f"\n---\n\n## {ticker}\n")

        for i, question in enumerate(EVALUATION_QUESTIONS[ticker], start=1):
            year = (
                EVAL_YEAR_BY_TICKER_Q1[ticker] if i == 1
                else EVAL_YEAR_BY_TICKER_Q2[ticker]
            )
            if (ticker, year) not in available:
                print(f"  [skip] {ticker} {year}: not in vector store")
                continue

            asked += 1
            print(f"[{asked}/{total}] {ticker} {year} Q{i}: "
                  f"{question[:80]}...")
            try:
                answer, best_node, _ = rag.respond(question, ticker, year)
            except Exception as e:
                answer = f"ERROR: {e}"
                best_node = None

            lines.append(f"### Question {i} -- Fiscal Year {year}\n")
            lines.append(f"**Q:** {question}\n")

            if best_node is not None:
                snippet = best_node.get_content()[:600].strip()
                lines.append(
                    "**Top retrieved chunk (truncated to 600 chars):**\n"
                )
                lines.append("```\n" + snippet + "\n```\n")
            else:
                lines.append("**Top retrieved chunk:** (none)\n")

            lines.append(f"**Generated answer:**\n\n{answer}\n")

    elapsed = time.time() - t0
    lines.append(f"\n---\n\n_Evaluation completed in {elapsed:.1f}s._\n")

    with open(EVAL_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nEvaluation written to {EVAL_OUTPUT_FILE}")
    print(f"Total questions: {asked}  |  Total time: {elapsed:.1f}s")


if __name__ == "__main__":
    run_evaluation()