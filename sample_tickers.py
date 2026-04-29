"""
sample_tickers.py

Sample 10 S&P 500 tickers deterministically using student ID as the random seed.
Tickers known to lack 2010-2019 filing history (e.g. post-2010 IPOs) are excluded
and replaced by continuing the seeded random draw, per the assignment instructions:
    "If a company does not have a complete 10-year history, exclude it from the
     sample and continue until 10 valid companies are selected."

The chosen tickers are written to `sampled_tickers.txt`, one ticker per line.

Author: Anay Abhijit Joshi
Student ID: 904168649
"""

import io
import random

import pandas as pd
import requests


STUDENT_ID: int = 904168649
NUM_DOCS: int = 10
WIKIPEDIA_URL: str = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
OUTPUT_FILE: str = "sampled_tickers.txt"

# Wikipedia rejects urllib's default User-Agent with HTTP 403, so we send a
# real header that identifies the requester per Wikipedia API etiquette.
USER_AGENT: str = (
    "AS6-RAG-Assignment/1.0 (Anay Abhijit Joshi; ajoshi498@gatech.edu) "
    "Mozilla/5.0 (Macintosh; Apple Silicon)"
)

# Tickers that exist in the current S&P 500 but lack a complete 2010-2019
# 10-K history (typically because they IPO'd after 2010-01-01).
KNOWN_INVALID: set[str] = {
    "GDDY",  # GoDaddy: IPO April 1, 2015 -- no 2010-2014 filings
}


def get_sp500_tickers_wikipedia() -> list[str]:
    """Scrape the current S&P 500 constituent list from Wikipedia."""
    response = requests.get(
        WIKIPEDIA_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(io.StringIO(response.text))
    sp500_table = tables[0]
    return sp500_table["Symbol"].tolist()


def sample_valid_tickers(tickers: list[str]) -> list[str]:
    """
    Pick NUM_DOCS tickers using STUDENT_ID as the RNG seed, replacing any
    that are in KNOWN_INVALID by drawing further from the same seeded
    random sequence. Reproducible end-to-end.
    """
    random.seed(STUDENT_ID)
    initial = random.sample(tickers, NUM_DOCS)

    # Keep the valid initial picks.
    final = [t for t in initial if t not in KNOWN_INVALID]

    # If any were excluded, draw replacements deterministically from the
    # remaining tickers using the same RNG state.
    if len(final) < NUM_DOCS:
        used = set(initial) | KNOWN_INVALID
        remaining = [t for t in tickers if t not in used]
        random.shuffle(remaining)  # uses the same seeded RNG state
        while len(final) < NUM_DOCS:
            final.append(remaining.pop(0))

    return final


def main() -> None:
    tickers = get_sp500_tickers_wikipedia()
    print(f"Loaded {len(tickers)} S&P 500 tickers from Wikipedia.")

    final = sample_valid_tickers(tickers)
    sampled = sorted(final)

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(sampled))

    print(f"\nSampled {NUM_DOCS} tickers (seed={STUDENT_ID}):")
    for ticker in sampled:
        print(f"  - {ticker}")
    if KNOWN_INVALID:
        excluded = KNOWN_INVALID & set(random.Random(STUDENT_ID).sample(tickers, NUM_DOCS))
        if excluded:
            print(f"\nExcluded (post-2010 IPO, no full history): {sorted(excluded)}")
    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()