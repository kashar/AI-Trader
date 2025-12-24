#!/usr/bin/env python3
"""
Fetch forex pair price data using Alpha Vantage API
Supports major currency pairs and precious metals (XAUUSD, XAGUSD)
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("ALPHAADVANTAGE_API_KEY")

if not API_KEY:
    print("Error: ALPHAADVANTAGE_API_KEY not set in .env file")
    sys.exit(1)

# Forex pairs to fetch
# Major pairs
MAJOR_PAIRS = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"]

# Precious metals
PRECIOUS_METALS = ["XAUUSD", "XAGUSD"]

# Default forex pairs (excluding metals for free tier)
DEFAULT_FOREX_PAIRS = MAJOR_PAIRS[:5]  # EUR, GBP, JPY, CHF, AUD


def parse_forex_pair(pair):
    """
    Parse forex pair symbol for Alpha Vantage API

    Args:
        pair: Forex pair symbol (e.g., "EURUSD", "XAUUSD")

    Returns:
        tuple: (from_currency, to_currency)
    """
    # Special handling for precious metals
    if pair == "XAUUSD":
        return ("XAU", "USD")  # Gold
    elif pair == "XAGUSD":
        return ("XAG", "USD")  # Silver
    elif pair == "XPTUSD":
        return ("XPT", "USD")  # Platinum
    elif pair == "XPDUSD":
        return ("XPD", "USD")  # Palladium

    # Standard currency pairs (assume 3-letter codes)
    if len(pair) == 6:
        return (pair[:3], pair[3:])
    else:
        raise ValueError(f"Invalid forex pair format: {pair}")


def fetch_forex_data(from_currency, to_currency, outputsize="full"):
    """
    Fetch forex data from Alpha Vantage

    Args:
        from_currency: Base currency (e.g., "EUR")
        to_currency: Quote currency (e.g., "USD")
        outputsize: 'compact' (100 datapoints) or 'full' (20+ years)

    Returns:
        dict: Price data
    """
    # Use different endpoint for precious metals
    is_metal = from_currency in ["XAU", "XAG", "XPT", "XPD"]

    url = "https://www.alphavantage.co/query"

    if is_metal:
        # Use COMMODITY endpoint for metals (not available in free tier)
        # Fallback: skip metals for now
        print(f"  ⚠️  Precious metals require premium API, skipping {from_currency}/{to_currency}")
        return None

    params = {
        "function": "FX_DAILY",
        "from_symbol": from_currency,
        "to_symbol": to_currency,
        "apikey": API_KEY,
        "outputsize": outputsize,
    }

    print(f"Fetching {from_currency}/{to_currency}...")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if "Error Message" in data:
            print(f"  ❌ API Error: {data['Error Message']}")
            return None
        if "Note" in data:
            print(f"  ⚠️ API Note: {data['Note']}")
            return None

        # Check if we got valid data
        if "Time Series FX (Daily)" not in data:
            print(f"  ❌ No time series data received")
            print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
            return None

        print(f"  ✅ Successfully fetched data")
        return data

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON decode error: {e}")
        return None


def save_forex_data(pair, data, output_dir="data/forex"):
    """
    Save forex data to JSON file

    Args:
        pair: Forex pair symbol
        data: Price data from API
        output_dir: Output directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = output_path / f"daily_prices_{pair}.json"

    # Convert to format compatible with existing tools
    formatted_data = {
        "Meta Data": {
            "1. Information": "Forex Daily Prices (open, high, low, close)",
            "2. Symbol": pair,
            "3. Last Refreshed": data["Meta Data"]["5. Last Refreshed"],
            "4. Time Zone": data["Meta Data"]["6. Time Zone"]
        },
        "Time Series (Daily)": {}
    }

    # Reformat time series data
    for date, prices in data["Time Series FX (Daily)"].items():
        formatted_data["Time Series (Daily)"][date] = {
            "1. buy price": prices["1. open"],
            "2. high": prices["2. high"],
            "3. low": prices["3. low"],
            "4. sell price": prices["4. close"],
            "5. volume": "0"  # Forex doesn't have volume, set to 0
        }

    with open(filename, "w") as f:
        json.dump(formatted_data, f, indent=2)

    print(f"  💾 Saved to {filename}")


def main():
    """Main function to fetch all forex pair data"""
    print("=" * 60)
    print("Forex Data Fetcher")
    print("=" * 60)
    print(f"API Key: {'*' * 20}{API_KEY[-4:]}")
    print(f"Pairs to fetch: {', '.join(DEFAULT_FOREX_PAIRS)}")
    print("=" * 60)

    # Create output directory
    output_dir = Path("data/forex")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch data for each pair
    for i, pair in enumerate(DEFAULT_FOREX_PAIRS):
        print(f"\n[{i+1}/{len(DEFAULT_FOREX_PAIRS)}] Processing {pair}:")

        try:
            from_curr, to_curr = parse_forex_pair(pair)
            data = fetch_forex_data(from_curr, to_curr)

            if data:
                save_forex_data(pair, data, output_dir)
            else:
                print(f"  ⚠️  Skipping {pair} due to fetch error")

            # Rate limiting: Alpha Vantage free tier allows 5 API requests per minute
            if i < len(DEFAULT_FOREX_PAIRS) - 1:
                print("  ⏳ Waiting 15 seconds (rate limiting)...")
                time.sleep(15)

        except Exception as e:
            print(f"  ❌ Error processing {pair}: {e}")
            continue

    print("\n" + "=" * 60)
    print("✅ Forex data fetching completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
