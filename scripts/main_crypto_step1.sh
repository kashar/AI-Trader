#!/bin/bash

# Crypto Data Preparation

# Get project root directory (parent of scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Ensure data/crypto exists and enter it
mkdir -p "$PROJECT_ROOT/data/crypto"
cd "$PROJECT_ROOT/data/crypto" || { echo "Cannot enter directory $PROJECT_ROOT/data/crypto"; exit 1; }

# Print current working directory before running python
echo "Current directory: $(pwd)"
echo "About to run: python get_daily_price_crypto.py"
python get_daily_price_crypto.py

echo "Current directory: $(pwd)"
echo "About to run: python merge_crypto_jsonl.py"
python merge_crypto_jsonl.py

# # for tushare
# echo "Current directory: $(pwd)"
# echo "About to run: python get_daily_price_tushare.py"
# python get_daily_price_tushare.py
# echo "Current directory: $(pwd)"
# echo "About to run: python merge_jsonl_tushare.py"
# python merge_jsonl_tushare.py

cd ..
