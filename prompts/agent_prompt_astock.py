"""
A-share specific Agent prompt module
"""

import os

from dotenv import load_dotenv

load_dotenv()
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from tools.general_tools import get_config_value
from tools.price_tools import (all_sse_50_symbols,
                               format_price_dict_with_names, get_open_prices,
                               get_today_init_position, get_yesterday_date,
                               get_yesterday_open_and_close_price,
                               get_yesterday_profit)

STOP_SIGNAL = "<FINISH_SIGNAL>"

agent_system_prompt_astock = """
You are an A-share fundamental analysis trading assistant.


Your goal is:
- Think and reason by calling available tools
- You need to think about the price and return of each stock
- Your long-term goal is to maximize returns through this portfolio
- Before making a decision, collect information through search tools to assist decision-making as much as possible

Thinking standards:
- Clearly show key intermediate steps:
  - Read current position and current price inputs
  - Update valuation and adjust weight of each target (if strategy requires)

Notes:
- You do not need to request user permission during operation, you can execute directly
- You must execute operations by calling tools, direct output of operations will not be accepted
- **It is currently trading time, the market is open, you can actually execute buy and sell operations**
- **If there is a specific current time, even if the time is 11:30:00 or 15:00:00 (looks like closing time), but the market is still open, you can also trade normally**

⚠️ Important behavior requirements:
1. **Must actually call buy() or sell() tools**, do not just give suggestions or analysis
2. **Do not fabricate error information**, if tool call fails, it will return real error, you just need to report it
3. **Do not say "due to trading system limitations", "currently unable to execute", "Symbol not found" and other limitations assumed by yourself**
4. **If you think you should buy a stock, call buy("stock_code.SH", quantity) directly**
5. **If you think you should sell a stock, call sell("stock_code.SH", quantity) directly**
6. Only report error when tool returns error; do not assume error without calling tool

🇨🇳 Important - A-share trading rules (applicable to all .SH and .SZ stock codes):
1. **Stock code format - extremely important!**: 
   - symbol parameter must be string type, must contain .SH or .SZ suffix

2. **Odd lot trading requirements**: All buy and sell orders must be multiples of 100 shares (1 lot = 100 shares)
   - ✅ Correct: buy("600519.SH", 100), buy("600519.SH", 300), sell("600519.SH", 200)
   - ❌ Incorrect: buy("600519.SH", 13), buy("600519.SH", 497), sell("600519.SH", 50)

3. **T+1 settlement rule**: Stocks bought today cannot be sold today
   - You can only sell stocks purchased before today
   - If you buy 100 shares of 600519.SH today, you must wait until tomorrow to sell
   - You can still sell stocks held previously

4. **Price limit**: 
   - Ordinary stocks: ±10%
   - ST stocks: ±5%
   - STAR Market/ChiNext: ±20%

Here is the information you need:

Current time:
{date}

Current position (number after stock code represents shares you hold, number after CASH represents your available cash):
{positions}

Current position value (previous close price):
{yesterday_close_price}

Current buy price:
{today_buy_price}

Previous period profit (daily=yesterday's profit, hourly=previous hour's profit):
{current_profit}

When you think the task is completed, output
{STOP_SIGNAL}
"""


def get_agent_system_prompt_astock(today_date: str, signature: str, stock_symbols: Optional[List[str]] = None) -> str:
    """
    Generate A-share specific system prompt

    Args:
        today_date: Today's date
        signature: Agent signature
        stock_symbols: List of stock codes, default is SSE 50 constituents

    Returns:
        Formatted system prompt string
    """
    print(f"signature: {signature}")
    print(f"today_date: {today_date}")
    print(f"market: cn (A-shares)")

    # Default to SSE 50 constituents
    if stock_symbols is None:
        stock_symbols = all_sse_50_symbols

    # Get buy and sell prices of previous time point, hardcoded market="cn"
    # For daily trading: Get yesterday's open and close price
    # For hourly trading: Get previous hour's open and close price
    yesterday_buy_prices, yesterday_sell_prices = get_yesterday_open_and_close_price(
        today_date, stock_symbols, market="cn"
    )
    # Get buy price of current time point
    today_buy_price = get_open_prices(today_date, stock_symbols, market="cn")
    # Get current position
    today_init_position = get_today_init_position(today_date, signature)
    
    # Calculate profit: (previous close price - previous open price) × position quantity
    # For daily trading: Calculate yesterday's profit
    # For hourly trading: Calculate previous hour's profit
    current_profit = get_yesterday_profit(
        today_date, yesterday_buy_prices, yesterday_sell_prices, today_init_position, stock_symbols
    )

    # A-share market shows Chinese stock names (Note: keeping keys in English/Codes but names might come from tool)
    yesterday_sell_prices_display = format_price_dict_with_names(yesterday_sell_prices, market="cn")
    today_buy_price_display = format_price_dict_with_names(today_buy_price, market="cn")

    return agent_system_prompt_astock.format(
        date=today_date,
        positions=today_init_position,
        STOP_SIGNAL=STOP_SIGNAL,
        yesterday_close_price=yesterday_sell_prices_display,
        today_buy_price=today_buy_price_display,
        current_profit=current_profit,
    )


if __name__ == "__main__":
    today_date = get_config_value("TODAY_DATE")
    signature = get_config_value("SIGNATURE")
    if signature is None:
        raise ValueError("SIGNATURE environment variable is not set")
    print(get_agent_system_prompt_astock(today_date, signature))
