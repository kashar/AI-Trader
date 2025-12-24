#!/bin/bash

# Get project root directory (parent of scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

echo "🤖 Starting main trading agent (A-share mode)..."

python main.py configs/astock_config.json  # Run A-share config

echo "✅ AI-Trader stopped"
