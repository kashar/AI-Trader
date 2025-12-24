#!/usr/bin/env python3
import json
import numpy as np
import sys
from pathlib import Path

# Add project root to path for importing result_tools
project_root = Path(__file__).resolve().parents[2]  # data/crypto -> AI-Trader
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tools.result_tools import (
    calculate_daily_returns, calculate_sharpe_ratio, calculate_max_drawdown,
    calculate_cumulative_return, calculate_volatility, calculate_win_rate
)

# Read CD5 index data
with open('CD5_crypto_index.json', 'r') as f:
    data = json.load(f)

time_series = data['Time Series (Daily)']
dates = sorted(time_series.keys())

# Filter data from 11-01, start from 11-02 to align with agent simulation time
agent_start_date = "2025-11-02"
if agent_start_date in dates:
    start_index = dates.index(agent_start_date)
    dates = dates[start_index:]
    print(f'⚠️ Time alignment: Skip 11-01, start from {agent_start_date} to align with agent simulation')
else:
    print(f'⚠️ {agent_start_date} data not found, using all available data')

print('=== CD5 Index Analysis (Aligned with Agent Time) ===')
print(f'Data Date Range: {dates[0]} to {dates[-1]}')
print(f'Total Trading Days: {len(dates)}')

# Calculate CD5 index performance (consistent with result_tools.py, using close price)
# Build portfolio value dict (consistent with result_tools.py format)
portfolio_values = {}
for date in dates:
    portfolio_values[date] = float(time_series[date]['4. close'])

initial_value = portfolio_values[dates[0]]  # Use first day close price, consistent with result_tools.py
final_value = portfolio_values[dates[-1]]  # Use last day close price

print(f'Initial Value: ${initial_value:,.2f}')
print(f'Final Value: ${final_value:,.2f}')
print(f'Value Change: ${final_value - initial_value:,.2f}')

# Use result_tools.py functions to calculate metrics, ensuring consistency
from datetime import datetime

# Calculate metrics (fully consistent with result_tools.py)
daily_returns = calculate_daily_returns(portfolio_values)
volatility = calculate_volatility(daily_returns, trading_days=365)  # Crypto 365 days
win_rate = calculate_win_rate(daily_returns)
sharpe_ratio = calculate_sharpe_ratio(daily_returns, trading_days=365)  # Crypto 365 days
max_drawdown, drawdown_start, drawdown_end = calculate_max_drawdown(portfolio_values)

# Use result_tools.py cumulative return function for consistency
cumulative_return = calculate_cumulative_return(portfolio_values)
print(f'Cumulative Return: {cumulative_return:.2%} (calculated by result_tools.py)')

# Calculate annualized return
start_date = datetime.strptime(dates[0], "%Y-%m-%d")
end_date = datetime.strptime(dates[-1], "%Y-%m-%d")
days = (end_date - start_date).days

if days > 0:
    annualized_return = (1 + cumulative_return) ** (365 / days) - 1
else:
    annualized_return = 0.0

print(f'Annualized Return: {annualized_return:.2%}')
print(f'Investment Days: {days} days')
print(f'Max Drawdown: {max_drawdown:.2%}')
print(f'Drawdown Period: {drawdown_start} to {drawdown_end}')
print(f'Annualized Volatility: {volatility:.2%}')
print(f'Sharpe Ratio: {sharpe_ratio:.4f}')
print(f'Win Rate: {win_rate:.2%}')

# Keep original variable names for compatibility
daily_volatility = np.std(daily_returns, ddof=1) if daily_returns else 0.0
mean_return = np.mean(daily_returns) if daily_returns else 0.0
annualized_return_for_sharpe = mean_return * 365
risk_free_rate = 0.02

# portfolio_values already built above, no need to repeat

# 输出用于报告的数据
print(f'\n=== Data for Report ===')
print(f'CD5 Index:')
print(f'  Cumulative Return: {cumulative_return:.2%}')
print(f'  Annualized Return: {annualized_return:.2%}')
print(f'  Sharpe Ratio: {sharpe_ratio:.4f}')
print(f'  Max Drawdown: {max_drawdown:.2%}')
print(f'  Win Rate: {win_rate:.2%}')
print(f'  Final Value: ${final_value:,.0f}')

# Save CD5 results to JSON file
save_cd5_results = True
if save_cd5_results:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'CD5_metrics_{timestamp}.json'

    cd5_results = {
        "evaluation_time": datetime.now().isoformat(),
        "model_name": "CD5 Index",
        "market": "crypto",
        "trading_days": len(dates),
        "start_date": dates[0],
        "end_date": dates[-1],
        "initial_value": initial_value,
        "final_value": final_value,
        "value_change": final_value - initial_value,
        "cumulative_return": round(cumulative_return, 4),
        "annualized_return": round(annualized_return, 4),
        "sharpe_ratio": round(sharpe_ratio, 4),
        "max_drawdown": round(max_drawdown, 4),
        "max_drawdown_start": drawdown_start,
        "max_drawdown_end": drawdown_end,
        "volatility": round(volatility, 4),
        "win_rate": round(win_rate, 4),
        "trading_days_with_data": len(daily_returns),
        "investment_days": days,
        "daily_returns_count": len(daily_returns),
        "daily_volatility": round(daily_volatility, 6),
        "mean_daily_return": round(mean_return, 6),
        "annualized_return_for_sharpe": round(annualized_return_for_sharpe, 4),
        "risk_free_rate": risk_free_rate,
        "trading_days_per_year": 365,  # Crypto 365 days trading
        "cd5_composition": {
            "BTC": 74.56,
            "ETH": 15.97,
            "XRP": 5.20,
            "SOL": 3.53,
            "ADA": 0.76
        },
        "notes": "CD5 Index benchmark, using 365 trading days for annualized metrics"
    }

    # Save detailed results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cd5_results, f, indent=2, ensure_ascii=False)

    print(f'\n💾 CD5 metrics saved to: {output_file}')

    # Also save a fixed name latest results file
    latest_file = 'CD5_latest_metrics.json'
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(cd5_results, f, indent=2, ensure_ascii=False)

    print(f'💾 Latest CD5 metrics saved to: {latest_file}')

    # Generate simplified data for report
    report_data = {
        "model_name": "CD5 Index",
        "status": "✅ Benchmark",
        "trading_days": len(dates),
        "start_date": dates[0],
        "end_date": dates[-1],
        "cumulative_return": round(cumulative_return, 4),
        "annualized_return": round(annualized_return, 4),
        "sharpe_ratio": round(sharpe_ratio, 4),
        "max_drawdown": round(max_drawdown, 4),
        "volatility": round(volatility, 4),
        "win_rate": round(win_rate, 4),
        "initial_value": initial_value,
        "final_value": final_value,
        "value_change": final_value - initial_value,
        "value_change_percent": round(cumulative_return, 4),
        "is_benchmark": True
    }

    # Save simplified version for model comparison
    report_file = 'CD5_for_comparison.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f'💾 Comparison CD5 data saved to: {report_file}')
else:
    print('\n⚠️ CD5 result saving disabled')