"""
data_downloading.py

Download all 10-K filings for the sampled tickers from SEC EDGAR for fiscal
years 2010-2019 inclusive (i.e. filing date >= 2010-01-01 and < 2020-01-01).

Filings are saved by sec-edgar-downloader into:
    {ORIGINAL_DATA_DIR}/sec-edgar-filings/{TICKER}/10-K/{accession-number}/

Author: Anay Abhijit Joshi
Student ID: 904168649
"""

import os
import time

from sec_edgar_downloader import Downloader

from config import ORIGINAL_DATA_DIR


# SEC EDGAR's fair-access policy requires a real name and email in the
# User-Agent string. They will rate-limit or block anonymous traffic.
SEC_USER_NAME: str = "Anay Abhijit Joshi"
SEC_USER_EMAIL: str = "ajoshi498@gatech.edu"

# Date window per the assignment: 2010 inclusive to 2020 exclusive.
START_DATE: str = "2010-01-01"
END_DATE: str = "2019-12-31"

# Small pause between tickers; sec-edgar-downloader already throttles
# at the per-request level, but this keeps us comfortably under SEC's cap.
SLEEP_BETWEEN_TICKERS: float = 1.0

TICKERS_FILE: str = "sampled_tickers.txt"


def load_tickers(path: str = TICKERS_FILE) -> list[str]:
    """Read sampled tickers, one per line."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Run sample_tickers.py first."
        )
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def download_all(tickers: list[str]) -> None:
    """Download 10-Ks for every ticker into ORIGINAL_DATA_DIR."""
    # The Downloader writes into <download_folder>/sec-edgar-filings/...
    dl = Downloader(SEC_USER_NAME, SEC_USER_EMAIL, ORIGINAL_DATA_DIR)

    for i, ticker in enumerate(tickers, start=1):
        print(f"[{i}/{len(tickers)}] Downloading 10-Ks for {ticker} "
              f"({START_DATE} to {END_DATE}) ...")
        try:
            num_downloaded = dl.get(
                "10-K",
                ticker,
                after=START_DATE,
                before=END_DATE,
            )
            print(f"    -> {num_downloaded} filing(s) retrieved.")
        except Exception as e:
            print(f"    !! Failed for {ticker}: {e}")

        time.sleep(SLEEP_BETWEEN_TICKERS)


def report_summary() -> None:
    """Print a concise per-ticker count of downloaded filings."""
    base = os.path.join(ORIGINAL_DATA_DIR, "sec-edgar-filings")
    if not os.path.isdir(base):
        print(f"\nNo filings directory found at {base}.")
        return

    print("\nDownload summary:")
    print(f"{'Ticker':<8} {'10-K filings':>14}")
    print("-" * 24)
    total = 0
    for ticker in sorted(os.listdir(base)):
        ten_k_dir = os.path.join(base, ticker, "10-K")
        if not os.path.isdir(ten_k_dir):
            continue
        count = sum(
            1 for entry in os.listdir(ten_k_dir)
            if os.path.isdir(os.path.join(ten_k_dir, entry))
        )
        total += count
        print(f"{ticker:<8} {count:>14}")
    print("-" * 24)
    print(f"{'TOTAL':<8} {total:>14}")


def main() -> None:
    tickers = load_tickers()
    print(f"Loaded {len(tickers)} tickers: {tickers}\n")

    download_all(tickers)
    report_summary()


if __name__ == "__main__":
    main()