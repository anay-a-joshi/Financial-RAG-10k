"""
data_processing.py

Convert raw SEC submissions (full-submission.txt) into clean per-filing text
files at PROCESSED_DATA_DIR/{ticker}_{year}/content.txt.

Pipeline per filing:
  1. Read full-submission.txt.
  2. Parse SEC header to extract CONFORMED PERIOD OF REPORT -> fiscal year.
  3. Locate the 10-K body:
       - Prefer <TYPE>10-K with an HTML filename (.htm/.html), not PDF.
       - Trim non-HTML preamble (binary blobs, base64 PDFs) before parsing.
       - Fall back to the largest HTML attachment if needed.
  4. Strip XBRL fragments, scripts, styles, hidden elements.
  5. Convert HTML into readable text while preserving headings and tables.
  6. Collapse whitespace and remove obvious SEC boilerplate.
  7. Write to PROCESSED_DATA_DIR/{ticker}_{year}/content.txt.

Author: Anay Abhijit Joshi
Student ID: 904168649
"""

import os
import re
from typing import Optional

from bs4 import BeautifulSoup

from config import ORIGINAL_DATA_DIR, PROCESSED_DATA_DIR


# Paths
FILINGS_ROOT: str = os.path.join(ORIGINAL_DATA_DIR, "sec-edgar-filings")

# Regex helpers
RE_PERIOD = re.compile(
    r"CONFORMED PERIOD OF REPORT:\s*(\d{8})", re.IGNORECASE
)
RE_DOC_BLOCK = re.compile(
    r"<DOCUMENT>(.*?)</DOCUMENT>", re.DOTALL | re.IGNORECASE
)
RE_DOC_TYPE = re.compile(r"<TYPE>([^\s<]+)", re.IGNORECASE)
RE_DOC_FILENAME = re.compile(r"<FILENAME>([^\s<]+)", re.IGNORECASE)
RE_TEXT_BLOCK = re.compile(
    r"<TEXT>(.*?)</TEXT>", re.DOTALL | re.IGNORECASE
)

# Used to locate where the actual HTML content starts inside a <TEXT>
# block. SEC <TEXT> blocks frequently begin with PDF binaries, base64
# blobs, or SGML preambles (<XBRL>, <PDF>...) that BeautifulSoup chokes
# on. We seek forward to the first real HTML opener.
RE_HTML_START = re.compile(
    r"<\s*(html|body|head|div|table|p|font|h1|h2|h3|span)\b",
    re.IGNORECASE,
)
# Detect filings that are stored as base64 PDFs inside <TEXT>.
RE_BASE64_PDF = re.compile(
    r"begin\s+\d+\s+\S+\.pdf|<PDF>", re.IGNORECASE
)

# Threshold below which a <TEXT> block is too small to be a real 10-K.
MIN_HTML_SIZE: int = 50_000

# Final cleaned-text size threshold for warnings.
MIN_CLEAN_TEXT_SIZE: int = 50_000

# Boilerplate patterns
BOILERPLATE_PATTERNS = [
    re.compile(r"Table of Contents", re.IGNORECASE),
    re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE),
    re.compile(r"^\s*\d+\s*$", re.MULTILINE),
    re.compile(r"\(Mark One\)", re.IGNORECASE),
    re.compile(
        r"UNITED STATES SECURITIES AND EXCHANGE COMMISSION\s*"
        r"Washington,?\s*D\.?C\.?\s*\d{5}",
        re.IGNORECASE,
    ),
]

RE_MULTI_NEWLINE = re.compile(r"\n{3,}")
RE_TRAILING_SPACES = re.compile(r"[ \t]+\n")
RE_NONBREAKING_SPACE = re.compile(r"\xa0")


def parse_conformed_period(text: str) -> Optional[str]:
    m = RE_PERIOD.search(text)
    if not m:
        return None
    return m.group(1)[:4]


def _iter_documents(submission_text: str):
    """Yield (doc_type, filename, body) for every <DOCUMENT> block."""
    for doc_match in RE_DOC_BLOCK.finditer(submission_text):
        block = doc_match.group(1)
        type_match = RE_DOC_TYPE.search(block)
        fname_match = RE_DOC_FILENAME.search(block)
        text_match = RE_TEXT_BLOCK.search(block)
        if not (type_match and text_match):
            continue
        doc_type = type_match.group(1).strip().upper()
        filename = fname_match.group(1).strip() if fname_match else ""
        body = text_match.group(1)
        yield doc_type, filename, body


def _is_html_filename(filename: str) -> bool:
    f = filename.lower()
    return f.endswith(".htm") or f.endswith(".html")


def _trim_to_html(body: str) -> str:
    """
    Strip any non-HTML preamble (PDF binaries, base64 blobs, SGML
    artifacts) and return the substring starting at the first real HTML
    tag. Returns the original string if no HTML opener is found.
    """
    m = RE_HTML_START.search(body)
    if m:
        return body[m.start():]
    return body


def extract_10k_html(submission_text: str) -> Optional[str]:
    """
    Selection priority:
      1. <TYPE>10-K block with an HTML-extension filename and >= MIN_HTML_SIZE
         bytes (after trimming non-HTML preamble).
      2. <TYPE>10-K block of any extension with substantive content.
      3. <TYPE>10-K/A amendment with substantive content.
      4. Largest HTML attachment in the submission.
      5. Whatever 10-K block exists, even if small.
    """
    primary_html: list[str] = []      # 10-K with .htm/.html filename
    primary_other: list[str] = []     # 10-K with other filename (e.g. PDF)
    amendments: list[str] = []
    all_html_attachments: list[str] = []

    for doc_type, filename, body in _iter_documents(submission_text):
        # Skip blocks that are obviously base64 PDFs.
        if RE_BASE64_PDF.search(body[:1000]):
            continue

        trimmed = _trim_to_html(body)

        # Track HTML-looking attachments regardless of declared type.
        if _is_html_filename(filename) or trimmed != body:
            all_html_attachments.append(trimmed)

        if doc_type == "10-K":
            if _is_html_filename(filename):
                primary_html.append(trimmed)
            else:
                primary_other.append(trimmed)
        elif doc_type.startswith("10-K"):
            amendments.append(trimmed)

    # Strategy 1: 10-K with HTML extension, big enough
    candidates = [b for b in primary_html if len(b) >= MIN_HTML_SIZE]
    if candidates:
        return max(candidates, key=len)

    # Strategy 2: any 10-K block big enough
    candidates = [
        b for b in (primary_html + primary_other)
        if len(b) >= MIN_HTML_SIZE
    ]
    if candidates:
        return max(candidates, key=len)

    # Strategy 3: amendments
    candidates = [b for b in amendments if len(b) >= MIN_HTML_SIZE]
    if candidates:
        return max(candidates, key=len)

    # Strategy 4: largest HTML attachment of any type
    candidates = [
        b for b in all_html_attachments if len(b) >= MIN_HTML_SIZE
    ]
    if candidates:
        return max(candidates, key=len)

    # Strategy 5: last resort, return whatever we have
    fallback_pool = primary_html + primary_other + amendments
    if fallback_pool:
        return max(fallback_pool, key=len)
    return None


def _bs_to_text(html: str, parser: str) -> str:
    soup = BeautifulSoup(html, parser)

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Strip inline XBRL wrappers but keep their text.
    for tag in soup.find_all(re.compile(r"^ix:", re.IGNORECASE)):
        tag.unwrap()

    # Drop hidden elements.
    for tag in soup.find_all(style=re.compile(r"display\s*:\s*none", re.I)):
        tag.decompose()

    # Convert tables to tab-separated rows so numeric data stays aligned.
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [
                cell.get_text(strip=True)
                for cell in tr.find_all(["td", "th"])
            ]
            cells = [c for c in cells if c]
            if cells:
                rows.append("\t".join(cells))
        table.replace_with("\n".join(rows) + "\n")

    # Force newlines around block-level elements.
    for tag in soup.find_all(
        ["p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr"]
    ):
        tag.append("\n")

    return soup.get_text(separator=" ")


def html_to_clean_text(html: str) -> str:
    """
    Convert HTML into readable text. Try lxml first (fast, strict); if
    that produces suspiciously little output relative to input size,
    retry with html.parser (slower, more forgiving).
    """
    text = _bs_to_text(html, "lxml")
    # If lxml choked (output << input), retry with html.parser.
    if len(text) < max(5_000, len(html) // 200):
        text = _bs_to_text(html, "html.parser")
    return text


def normalize_whitespace(text: str) -> str:
    text = RE_NONBREAKING_SPACE.sub(" ", text)
    text = RE_TRAILING_SPACES.sub("\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = RE_MULTI_NEWLINE.sub("\n\n", text)
    return text.strip()


def remove_boilerplate(text: str) -> str:
    for pat in BOILERPLATE_PATTERNS:
        text = pat.sub("", text)
    return text


def process_filing(submission_path: str) -> Optional[tuple[str, str]]:
    with open(submission_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    year = parse_conformed_period(raw)
    if year is None:
        return None

    body_html = extract_10k_html(raw)
    if body_html is None:
        return None

    text = html_to_clean_text(body_html)
    text = remove_boilerplate(text)
    text = normalize_whitespace(text)
    return year, text


def process_all() -> None:
    if not os.path.isdir(FILINGS_ROOT):
        raise FileNotFoundError(
            f"{FILINGS_ROOT} not found. Run data_downloading.py first."
        )

    print(f"Processing filings under {FILINGS_ROOT}\n")

    summary: dict[str, list[str]] = {}
    failures: list[str] = []
    warnings: list[str] = []

    for ticker in sorted(os.listdir(FILINGS_ROOT)):
        ten_k_dir = os.path.join(FILINGS_ROOT, ticker, "10-K")
        if not os.path.isdir(ten_k_dir):
            continue

        summary[ticker] = []
        for accession in sorted(os.listdir(ten_k_dir)):
            sub_path = os.path.join(
                ten_k_dir, accession, "full-submission.txt"
            )
            if not os.path.isfile(sub_path):
                failures.append(f"{ticker}/{accession}: missing submission")
                continue

            result = process_filing(sub_path)
            if result is None:
                failures.append(
                    f"{ticker}/{accession}: could not extract 10-K body"
                )
                continue

            year, cleaned = result
            out_dir = os.path.join(
                PROCESSED_DATA_DIR, f"{ticker}_{year}"
            )
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "content.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            summary[ticker].append(year)
            flag = ""
            if len(cleaned) < MIN_CLEAN_TEXT_SIZE:
                flag = "  [!] suspiciously small"
                warnings.append(
                    f"{ticker} {year}: {len(cleaned):,} chars (under "
                    f"{MIN_CLEAN_TEXT_SIZE:,})"
                )
            print(
                f"  {ticker} {year}: {len(cleaned):>9,} chars -> {out_path}"
                f"{flag}"
            )

    print("\n" + "=" * 50)
    print("Processing summary:")
    print(f"{'Ticker':<8} {'Years':<6} {'Year list'}")
    print("-" * 50)
    for ticker in sorted(summary):
        years = sorted(summary[ticker])
        print(f"{ticker:<8} {len(years):<6} {', '.join(years)}")
    print("-" * 50)
    total = sum(len(v) for v in summary.values())
    print(f"Total processed filings: {total}")

    if warnings:
        print("\nSize warnings (still written, but may have parsing issues):")
        for w in warnings:
            print(f"  - {w}")

    if failures:
        print("\nFailures:")
        for line in failures:
            print(f"  - {line}")


if __name__ == "__main__":
    process_all()