# Forex Trading Agent - Quick Start Guide

## Overview

The AI-Trader now supports forex trading for major currency pairs and precious metals including:
- **Precious Metals**: XAUUSD (Gold), XAGUSD (Silver)
- **Major Pairs**: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD

## What Was Created

### 1. Core Agent (`agent/base_agent_forex/`)
- **BaseAgentForex**: Specialized forex trading agent class
- Supports all major currency pairs and precious metals
- Built-in forex market rules (24/5 trading, weekday only)
- Automatic position management and risk controls

### 2. Prompts (`prompts/agent_prompt_forex.py`)
- Forex-specific trading prompts
- Economic indicator awareness
- Central bank policy considerations
- Correlation and risk management guidance

### 3. Configuration (`configs/default_forex_config.json`)
- Pre-configured for 5 forex pairs:
  - XAUUSD (Gold/USD)
  - XAGUSD (Silver/USD)
  - EURUSD (Euro/USD)
  - GBPUSD (Pound/USD)
  - USDJPY (USD/Yen)
- Initial capital: $10,000
- Default model: GPT-5 (can be changed)

### 4. Data Infrastructure (`data/forex/`)
- **get_daily_price_forex.py**: Fetch forex data from Alpha Vantage
- **merge_jsonl_forex.py**: Convert to unified JSONL format
- **README.md**: Complete data documentation

---

## Quick Start

### Step 1: Set Up Environment

Ensure your `.env` file has the Alpha Vantage API key:

```bash
ALPHAADVANTAGE_API_KEY=your_alpha_vantage_key
OPENAI_API_KEY=your_openai_key
```

### Step 2: Fetch Forex Data

```bash
# Navigate to forex data directory
cd data/forex

# Fetch daily price data (takes ~5 minutes due to API rate limits)
python get_daily_price_forex.py

# Merge into unified format
python merge_jsonl_forex.py
```

Expected output:
```
✅ Successfully merged 5/5 forex pairs
📁 Output file: data/forex/forex_merged.jsonl
```

### Step 3: Start MCP Services

Make sure MCP services are running:

```bash
cd agent_tools
python start_mcp_services.py
```

Or use the convenience script:

```bash
bash scripts/main_step2.sh
```

### Step 4: Run Forex Trading Agent

```bash
# From project root
python main.py configs/default_forex_config.json
```

---

## Configuration Options

### Customize Forex Pairs

Edit `configs/default_forex_config.json`:

```json
{
  "agent_config": {
    "forex_pairs": [
      "XAUUSD",   // Gold
      "XAGUSD",   // Silver
      "EURUSD",   // Euro
      "GBPUSD",   // Pound
      "USDJPY",   // Yen
      "AUDUSD",   // Aussie Dollar
      "USDCAD"    // Canadian Dollar
    ]
  }
}
```

### Change Trading Period

```json
{
  "date_range": {
    "init_date": "2025-10-01",
    "end_date": "2025-10-31"
  }
}
```

### Select Different AI Model

```json
{
  "models": [
    {
      "name": "claude-3.7-sonnet",
      "signature": "claude-3.7-sonnet-forex",
      "enabled": true
    }
  ]
}
```

---

## Forex Market Characteristics

### Trading Hours
- **Open**: 24 hours, 5 days a week (Monday-Friday)
- **Closed**: Weekends (Saturday-Sunday)

### Default Pairs

**Precious Metals** (Safe-Haven Assets):
- XAUUSD: Gold tends to rise during uncertainty
- XAGUSD: Silver follows gold but more volatile

**Major Currency Pairs**:
- EURUSD: Most liquid pair, ~30% of forex volume
- GBPUSD: "Cable", heavily influenced by UK/EU economics
- USDJPY: Safe-haven pair, influenced by BoJ policy

### Key Factors Affecting Forex

1. **Economic Indicators**:
   - GDP, employment, inflation (CPI/PPI)
   - Interest rate decisions
   - Trade balance

2. **Central Bank Policies**:
   - Federal Reserve (USD)
   - European Central Bank (EUR)
   - Bank of England (GBP)
   - Bank of Japan (JPY)

3. **Geopolitical Events**:
   - Elections, wars, trade disputes
   - Brexit, US-China relations

4. **Technical Factors**:
   - Support/resistance levels
   - Moving averages
   - RSI, MACD indicators

---

## File Structure

```
AI-Trader/
├── agent/
│   └── base_agent_forex/
│       ├── __init__.py
│       └── base_agent_forex.py           # Forex agent class
├── prompts/
│   └── agent_prompt_forex.py             # Forex trading prompts
├── configs/
│   └── default_forex_config.json         # Forex configuration
├── data/
│   └── forex/
│       ├── get_daily_price_forex.py      # Data fetcher
│       ├── merge_jsonl_forex.py          # Data merger
│       ├── README.md                     # Data documentation
│       ├── daily_prices_*.json           # Individual pair data
│       └── forex_merged.jsonl            # Merged data
└── data/agent_data_forex/                # Trading logs
    └── {agent_signature}/
        ├── position/
        │   └── position.jsonl            # Position history
        └── log/
            └── {date}/
                └── log.jsonl             # Trading logs
```

---

## Performance Analysis

After running forex trading, analyze performance:

```bash
# Calculate metrics
source venv/bin/activate
python tools/calculate_metrics.py \
  data/agent_data_forex/gpt-5-forex/position/position.jsonl \
  --data-dir data/forex

# Generate visualizations
python tools/plot_metrics.py \
  data/agent_data_forex/gpt-5-forex/position/portfolio_values.csv
```

---

## Differences from Stock/Crypto Trading

### Forex-Specific Features

1. **No Volume**: Spot forex doesn't have traditional volume
2. **Pip-based Pricing**: Prices typically to 4-5 decimal places
3. **Bid-Ask Spread**: Wider spreads during low liquidity
4. **Leverage** (optional): Default 1:1, can be configured
5. **Rollover/Swap**: Interest on overnight positions (not yet implemented)

### Trading Considerations

1. **Liquidity**:
   - Highest during London/NY overlap (8 AM - 12 PM EST)
   - Lower on Fridays and before holidays

2. **Volatility**:
   - Precious metals can be very volatile
   - Major pairs are generally more stable
   - News releases cause sudden spikes

3. **Correlation**:
   - EUR and GBP often correlated
   - USD and Gold often inversely correlated
   - JPY strengthens during risk-off events

---

## Troubleshooting

### Issue: "No forex data found"
**Solution**: Run data fetching scripts
```bash
cd data/forex
python get_daily_price_forex.py
python merge_jsonl_forex.py
```

### Issue: "API rate limit exceeded"
**Solution**: Alpha Vantage free tier allows 5 requests/minute
- Wait 60 seconds and retry
- Or upgrade to premium tier

### Issue: "Agent not found in registry"
**Solution**: Ensure main.py includes BaseAgentForex in AGENT_REGISTRY

### Issue: "MCP services not running"
**Solution**:
```bash
cd agent_tools
python start_mcp_services.py
```

---

## Example Workflow

Complete end-to-end example:

```bash
# 1. Setup environment
cd /path/to/AI-Trader
source venv/bin/activate

# 2. Fetch forex data (one-time or periodic)
cd data/forex
python get_daily_price_forex.py
python merge_jsonl_forex.py
cd ../..

# 3. Start MCP services
cd agent_tools
python start_mcp_services.py &
cd ..

# 4. Run forex trading
python main.py configs/default_forex_config.json

# 5. Analyze results
python tools/calculate_metrics.py \
  data/agent_data_forex/gpt-5-forex/position/position.jsonl \
  --data-dir data/forex
```

---

## Advanced Usage

### Custom Forex Pairs

To add more pairs (e.g., exotic pairs):

1. Update `data/forex/get_daily_price_forex.py`:
```python
CUSTOM_PAIRS = ["USDTRY", "USDZAR", "USDMXN"]
```

2. Fetch and merge data
3. Update configuration

### Multiple Agents Comparison

Run multiple AI models on same data:

```json
{
  "models": [
    {"name": "gpt-5", "enabled": true},
    {"name": "claude-3.7-sonnet", "enabled": true},
    {"name": "qwen3-max", "enabled": true}
  ]
}
```

Compare performance across models!

---

## API Costs

### Alpha Vantage
- **Free**: 5 requests/minute, 500/day
- **Premium**: $50/month, 75 requests/minute, 15,000/day

### AI Model Costs
- GPT-5: ~$0.50-1.00 per trading day
- Claude Sonnet: ~$0.30-0.60 per trading day
- Qwen/DeepSeek: Varies by provider

---

## Future Enhancements

Planned features:
- [ ] Intraday/hourly forex trading
- [ ] Technical indicator integration
- [ ] Economic calendar integration
- [ ] Multi-timeframe analysis
- [ ] Position sizing based on volatility
- [ ] Stop-loss and take-profit orders
- [ ] Swap/rollover cost calculation
- [ ] More exotic pairs support

---

## Support

For questions or issues:
1. Check `data/forex/README.md` for data-specific help
2. Review main project README.md
3. Open GitHub issue with forex label

---

**Happy Forex Trading with AI-Trader! 🌍💱📈**
