#!/usr/bin/env python3
"""
Merge forex pair price data into unified JSONL format
Compatible with the existing trading framework
"""

import json
import os
from pathlib import Path


def merge_forex_jsonl(input_dir="data/forex", output_file="data/forex/forex_merged.jsonl"):
    """
    Merge all forex pair JSON files into a single JSONL file

    Args:
        input_dir: Directory containing individual forex pair JSON files
        output_file: Output JSONL file path
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)

    # Find all forex price JSON files
    json_files = sorted(input_path.glob("daily_prices_*.json"))

    if not json_files:
        print(f"❌ No forex price files found in {input_dir}")
        print(f"   Please run get_daily_price_forex.py first")
        return

    print("=" * 60)
    print("Forex Data Merger")
    print("=" * 60)
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_file}")
    print(f"Found {len(json_files)} forex pair files")
    print("=" * 60)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Process each forex pair file
    processed = 0
    with open(output_path, "w") as outfile:
        for json_file in json_files:
            try:
                # Extract forex pair from filename
                pair = json_file.stem.replace("daily_prices_", "")

                print(f"Processing {pair}... ", end="")

                # Load JSON data
                with open(json_file, "r") as f:
                    data = json.load(f)

                # Write to JSONL
                outfile.write(json.dumps(data) + "\n")

                print("✅")
                processed += 1

            except Exception as e:
                print(f"❌ Error: {e}")
                continue

    print("=" * 60)
    print(f"✅ Successfully merged {processed}/{len(json_files)} forex pairs")
    print(f"📁 Output file: {output_file}")

    # Show file size
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"📊 File size: {size_mb:.2f} MB")

    print("=" * 60)


if __name__ == "__main__":
    merge_forex_jsonl()
