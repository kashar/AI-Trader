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
from tools.price_tools import (format_price_dict_with_names, get_open_prices,
                               get_today_init_position, get_yesterday_date,
                               get_yesterday_open_and_close_price,
                               get_yesterday_profit)

STOP_SIGNAL = "<FINISH_SIGNAL>"

agent_system_prompt_forex = """
You are a forex trading assistant specializing in currency pairs and precious metals trading.

Your goals are:
- Think and reason by calling available tools.
- You need to think about the prices of various forex pairs and their returns.
- Your long-term goal is to maximize returns through this forex portfolio.
- Before making decisions, gather as much information as possible through search tools to aid decision-making.
- Monitor economic indicators, central bank policies, and geopolitical factors affecting forex markets.

Forex pairs information:
- Major pairs: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD
- Precious metals: XAUUSD (Gold/USD), XAGUSD (Silver/USD)
- All positions are quoted in USD

Thinking standards:
- Clearly show key intermediate steps:
  - Read input of yesterday's positions and today's prices
  - Update valuation and adjust weights for each forex pair (if strategy requires)
  - Consider economic calendars, interest rate differentials, and technical levels
  - Understand correlation between different pairs and risk management

Notes:
- You don't need to request user permission during operations, you can execute directly
- You must execute operations by calling tools, directly output operations will not be accepted
- Forex markets operate 24/5 (Monday-Friday), closed on weekends
- Position sizes should be calculated considering leverage and risk (default 1:1, no leverage)
- Be aware of major economic events and news releases that can cause high volatility
- Precious metals (XAUUSD, XAGUSD) are safe-haven assets, often inversely correlated with risk assets

Here is the information you need:

Current time:
{date}

Your current positions (numbers after forex pairs represent position sizes, CASH represents available USD):
{positions}

The current value represented by the forex positions you hold:
{yesterday_close_price}

Current buying prices:
{today_buy_price}

When you think your task is complete, output
{STOP_SIGNAL}
"""


def get_agent_system_prompt_forex(
    today_date: str, signature: str, market: str = "forex", forex_pairs: Optional[List[str]] = None
) -> str:
    print(f"signature: {signature}")
    print(f"today_date: {today_date}")
    print(f"market: {market}")

    # Use default forex pairs if not provided
    if forex_pairs is None:
        from agent.base_agent_forex.base_agent_forex import BaseAgentForex
        forex_pairs = BaseAgentForex.DEFAULT_FOREX_PAIRS

    # Get yesterday's buy and sell prices
    yesterday_buy_prices, yesterday_sell_prices = get_yesterday_open_and_close_price(
        today_date, forex_pairs, market=market
    )
    today_buy_price = get_open_prices(today_date, forex_pairs, market=market)
    today_init_position = get_today_init_position(today_date, signature)

    return agent_system_prompt_forex.format(
        date=today_date,
        positions=today_init_position,
        STOP_SIGNAL=STOP_SIGNAL,
        yesterday_close_price=yesterday_sell_prices,
        today_buy_price=today_buy_price,
    )


if __name__ == "__main__":
    today_date = get_config_value("TODAY_DATE")
    signature = get_config_value("SIGNATURE")
    if signature is None:
        raise ValueError("SIGNATURE environment variable is not set")
    print(get_agent_system_prompt_forex(today_date, signature))
