#!/bin/bash

# Get project root directory (parent of scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

echo "🤖 Now starting the cryptocurrencies trading agent..."

python main.py configs/default_crypto_config.json 

echo "✅ AI-Trader stopped"
