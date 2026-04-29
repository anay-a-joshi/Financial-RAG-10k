#!/usr/bin/env bash
set -euo pipefail

python data_downloading.py
python data_processing.py
python vector_store_construction.py
python system.py
