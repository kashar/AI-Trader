# Forex Trading Data

This directory contains forex pair price data for the AI-Trader forex trading module.

## Supported Forex Pairs

### Precious Metals
- **XAUUSD** - Gold/USD
- **XAGUSD** - Silver/USD

### Major Currency Pairs
- **EURUSD** - Euro/US Dollar
- **GBPUSD** - British Pound/US Dollar
- **USDJPY** - US Dollar/Japanese Yen
- **USDCHF** - US Dollar/Swiss Franc
- **AUDUSD** - Australian Dollar/US Dollar
- **USDCAD** - US Dollar/Canadian Dollar
- **NZDUSD** - New Zealand Dollar/US Dollar

## Data Fetching

### Prerequisites
- Alpha Vantage API key (set in `.env` as `ALPHAADVANTAGE_API_KEY`)

### Fetch Daily Price Data

```bash
cd data/forex
python get_daily_price_forex.py
```

This will:
1. Fetch daily OHLC data for all default forex pairs
2. Save individual JSON files: `daily_prices_XAUUSD.json`, `daily_prices_EURUSD.json`, etc.
3. Rate-limit requests to comply with API limits (5 requests/minute for free tier)

### Merge Data

```bash
python merge_jsonl_forex.py
```

This will:
1. Combine all individual JSON files into `forex_merged.jsonl`
2. Format data compatible with the trading framework

## Data Format

### Individual JSON Files
Each file contains:
- Meta Data: Symbol, last refresh date, timezone
- Time Series (Daily): Date-indexed OHLC prices

```json
{
  "Meta Data": {
    "1. Information": "Forex Daily Prices (open, high, low, close)",
    "2. Symbol": "XAUUSD",
    "3. Last Refreshed": "2025-11-07",
    "4. Time Zone": "US/Eastern"
  },
  "Time Series (Daily)": {
    "2025-11-07": {
      "1. buy price": "2620.50",
      "2. high": "2635.80",
      "3. low": "2610.20",
      "4. sell price": "2628.90",
      "5. volume": "0"
    }
  }
}
```

### Merged JSONL File
Each line contains one forex pair's complete data.

## Usage with AI-Trader

1. **Fetch data**:
   ```bash
   python data/forex/get_daily_price_forex.py
   python data/forex/merge_jsonl_forex.py
   ```

2. **Run forex trading agent**:
   ```bash
   python main.py configs/default_forex_config.json
   ```

## API Rate Limits

Alpha Vantage Free Tier:
- 5 API requests per minute
- 500 requests per day

The data fetching script automatically adds 15-second delays between requests to stay within limits.

## Data Storage

- Individual files: `data/forex/daily_prices_*.json`
- Merged data: `data/forex/forex_merged.jsonl`
- Trading logs: `data/agent_data_forex/`

## Notes

- Forex markets are open 24/5 (Monday-Friday)
- Data is updated daily during market hours
- Precious metals (XAUUSD, XAGUSD) are treated as forex pairs
- All prices are in USD
- Volume is set to "0" for forex (spot forex doesn't have volume)
