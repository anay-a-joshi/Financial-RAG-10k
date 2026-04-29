"""
app.py

Streamlit web interface for the Financial Statement RAG system.

Usage:
    streamlit run app.py

Author: Anay Abhijit Joshi
Student ID: 904168649
"""

import time
from typing import Optional

import streamlit as st

from system import RAGSystem


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="10-K Financial RAG",
    page_icon="📈",
    layout="centered",
)


# ---------------------------------------------------------------------------
# RAG system loader (cached for the lifetime of the Streamlit session)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading the RAG system (one-time)...")
def get_system() -> RAGSystem:
    """
    Load the RAG system exactly once per Streamlit session.

    The embedding model and Chroma client are heavyweight; without
    caching, every interaction would reload them.
    """
    return RAGSystem(use_reranker=False)


@st.cache_data(show_spinner=False)
def get_filing_options(_system: RAGSystem) -> dict[str, list[str]]:
    """
    Return a {ticker: [year, ...]} mapping of every filing in the
    vector store. Cached so we don't re-scan Chroma on every rerun.

    The leading underscore on `_system` tells Streamlit not to hash
    the system object itself (it isn't hashable).
    """
    pairs = _system.get_available_filings()
    grouped: dict[str, list[str]] = {}
    for ticker, year in pairs:
        grouped.setdefault(ticker, []).append(year)
    for t in grouped:
        grouped[t].sort()
    return grouped


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("📈 Financial Statement Q&A")
st.caption(
    "Ask natural-language questions about a company's 10-K filing. "
    "Retrieval-Augmented Generation over SEC EDGAR data, running fully local."
)

# Load the system. Any failure here is fatal -- we surface a clear message.
try:
    system = get_system()
    filings = get_filing_options(system)
except Exception as exc:  # noqa: BLE001
    st.error(
        "Failed to initialize the RAG system. Make sure you have run "
        "`vector_store_construction.py` and that Ollama is running.\n\n"
        f"Details: {exc}"
    )
    st.stop()

if not filings:
    st.warning(
        "No filings found in the vector store. Run "
        "`vector_store_construction.py` first."
    )
    st.stop()


# --- Selection controls -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    ticker = st.selectbox(
        "Company (ticker)",
        options=sorted(filings.keys()),
        index=0,
        help="Choose one of the 10 sampled S&P 500 tickers.",
    )

with col2:
    year = st.selectbox(
        "Fiscal year",
        options=filings[ticker],
        index=len(filings[ticker]) - 1,  # default to most recent
        help="Fiscal year covered by the 10-K filing.",
    )

# --- Question input ---------------------------------------------------------
question = st.text_area(
    "Your question",
    placeholder=(
        f"e.g., What were the principal risk factors disclosed by "
        f"{ticker} in fiscal year {year}?"
    ),
    height=100,
)

submit = st.button("🔎 Ask", type="primary", use_container_width=True)


# --- Run pipeline -----------------------------------------------------------
if submit:
    if not question.strip():
        st.warning("Please enter a question before submitting.")
        st.stop()

    with st.spinner(
        f"Retrieving relevant context from {ticker} {year} 10-K and "
        f"generating an answer..."
    ):
        t0 = time.time()
        try:
            answer, best_node, all_nodes = system.respond(
                question, ticker, year
            )
            elapsed = time.time() - t0
        except Exception as exc:  # noqa: BLE001
            st.error(
                "Something went wrong while answering. This is most often "
                "caused by Ollama not running. Try `brew services start "
                "ollama` (or open the Ollama app) and ask again.\n\n"
                f"Details: {exc}"
            )
            st.stop()

    # --- Display answer ----------------------------------------------------
    st.markdown("### Answer")
    st.markdown(answer)
    st.caption(f"Generated in {elapsed:.1f}s.")

    # --- Display retrieved chunks for transparency / debugging -------------
    if all_nodes:
        with st.expander(
            f"📚 Show retrieved chunks ({len(all_nodes)})", expanded=False
        ):
            st.caption(
                "These are the top-k chunks the retriever pulled from the "
                "vector store and passed to the LLM as context. Useful for "
                "auditing whether the answer is grounded."
            )
            for i, node in enumerate(all_nodes, start=1):
                meta = node.metadata or {}
                ticker_m = meta.get("ticker", "?")
                year_m = meta.get("year", "?")
                chunk_idx = meta.get("chunk_index", "?")
                st.markdown(
                    f"**Chunk {i}** — `{ticker_m} {year_m}` "
                    f"(chunk #{chunk_idx})"
                )
                st.text_area(
                    label=f"chunk-{i}",
                    value=node.get_content(),
                    height=180,
                    label_visibility="collapsed",
                    key=f"chunk-{i}-{time.time()}",
                )
    else:
        st.info("No matching chunks were retrieved for this filing.")


# ---------------------------------------------------------------------------
# Footer / help
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### About")
    st.markdown(
        "**Anay Abhijit Joshi**  \n"
        "AS6 — Financial RAG  \n"
        "Student ID: 904168649"
    )
    st.markdown("---")
    st.markdown("### Pipeline")
    st.markdown(
        "- **Source:** SEC EDGAR 10-K filings (2009–2019)  \n"
        "- **Embedding:** `BAAI/bge-small-en-v1.5`  \n"
        "- **Vector store:** ChromaDB (persistent)  \n"
        "- **LLM:** `llama3.2:3b` via Ollama  \n"
        f"- **Filings indexed:** {sum(len(v) for v in filings.values())}  \n"
        f"- **Tickers:** {len(filings)}"
    )
    st.markdown("---")
    st.markdown("### Tips")
    st.markdown(
        "- Be specific: ask about products, segments, risks, financials.  \n"
        "- The system will say so if the answer isn't in the filing.  \n"
        "- Expand **'Show retrieved chunks'** to inspect the evidence."
    )