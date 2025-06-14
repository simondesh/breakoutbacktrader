# S&P 500 Breakout Strategy Backtest

A comprehensive Python example of using backtrader ; It compares a technical breakout strategy against a simple buy-and-hold approach using the S&P 500 index (SPY ETF).

## 📈 Strategy Overview

### Breakout Strategy
- **Entry Signal**: Buy when price breaks above the 20-period high
- **Exit Signals**:
  - Price breaks below the 20-period low
  - 5% stop-loss from entry price
  - 15% take-profit from entry price
- **Position Sizing**: Uses 95% of available cash per trade
- **Commission**: 0.1% per trade

### Buy-and-Hold Strategy
- **Entry**: Buy on the first trading day
- **Exit**: Hold until the end of the backtest period
- **Benchmark**: Used for performance comparison

## 🚀 Features

- **Real Market Data**: Downloads live S&P 500 data using Yahoo Finance
- **Comprehensive Analytics**: 
  - Total returns
  - Sharpe ratio
  - Maximum drawdown
  - Trade-by-trade analysis
- **Visual Analysis**: Side-by-side candlestick charts with trade markers
- **Performance Comparison**: Direct comparison between strategies
- **Detailed Logging**: All trades logged with entry/exit reasons and P&L

## 📋 Requirements

- see `requirements.txt` for dependencies

## 🔧 Installation

1. Clone or download the project files
2. Install the required dependencies:

```bash
pip install backtrader yfinance matplotlib pandas
```
or 
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Usage

Run the backtest with default parameters:

```bash
python breakout_backtest.py
```

The script will:
1. Download 2 years of S&P 500 historical data
2. Run both strategies with $100,000 starting capital
3. Display trade-by-trade execution logs
4. Show performance comparison results
5. Generate visualization charts

## ⚙️ Customization

### Strategy Parameters

You can modify the breakout strategy parameters in the `BreakoutStrategy` class:

```python
params = dict(
    lookback_period = 20,  # Number of periods to look back for high/low
    stop_loss = 0.05,      # 5% stop loss
    take_profit = 0.15,    # 15% take profit
)
```

### Backtest Settings

Adjust the backtest configuration in the `run_backtest()` function:
you can modify the start and end dates, the commission rate, initial cash, position sizing, etc.


## 📊 Output Examples

### Console Output
```
==================================================
RUNNING BREAKOUT STRATEGY
==================================================
BUY at 443.72 on 2023-07-18
SELL at 432.68 on 2023-08-15 - Breakout Exit - P&L: -2.49%
BUY at 431.97 on 2023-11-10
SELL at 499.57 on 2024-02-22 - Take Profit - P&L: 15.65%
BUY at 504.84 on 2024-03-01
SELL at 498.11 on 2024-04-15 - Breakout Exit - P&L: -1.33%
BUY at 513.63 on 2024-05-09
SELL at 536.15 on 2024-07-24 - Breakout Exit - P&L: 4.38%
BUY at 554.36 on 2024-08-19
SELL at 578.75 on 2025-01-10 - Breakout Exit - P&L: 4.40%
BUY at 604.62 on 2025-01-22
SELL at 583.30 on 2025-02-27 - Breakout Exit - P&L: -3.53%
BUY at 566.76 on 2025-05-02

==================================================
RUNNING BUY AND HOLD STRATEGY
==================================================
BUY AND HOLD at 430.80 on 2023-06-15

==================================================
BACKTEST RESULTS COMPARISON
==================================================

BREAKOUT STRATEGY:
Starting Portfolio Value: $100,000.00
Final Portfolio Value: $120,989.39
Total Return: 20.99%
Sharpe Ratio: 0.9458681046357603
Max Drawdown: 8.66%

BUY AND HOLD STRATEGY:
Starting Portfolio Value: $100,000.00
Final Portfolio Value: $136,026.65
Total Return: 36.03%
Sharpe Ratio: 1.104277151847276
Max Drawdown: 18.12%

PERFORMANCE DIFFERENCE:
Breakout vs Buy&Hold: -15.04% difference
```

## 📈 Visualization

The script generates two comprehensive charts:
- **Breakout Strategy Chart**: Shows entry/exit points, portfolio value over time
- **Buy-and-Hold Chart**: Baseline comparison with simple buy-and-hold approach


## 🔍 Key Metrics Explained

- **Total Return**: Overall percentage gain/loss from start to finish
- **Sharpe Ratio**: Risk-adjusted return measure (higher is better)
- **Max Drawdown**: Largest peak-to-trough decline during the period
- **Win Rate**: Percentage of profitable trades (displayed in trade logs)

## 🛠️ Extending the Code

### Adding New Strategies
Create a new strategy class inheriting from `bt.Strategy`:

```python
class YourCustomStrategy(bt.Strategy):
    def __init__(self):
        # Initialize indicators
        pass
    
    def next(self):
        # Define trading logic
        pass
```

### Adding More Analyzers
Enhance analysis with additional backtrader analyzers:

```python
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
cerebro.addanalyzer(bt.analyzers.VWR, _name='vwr')  # Variability-Weighted Return
```

### Testing Different Assets
Change the ticker symbol to test other assets:

```python
ticker = "QQQ"  # NASDAQ-100
ticker = "IWM"  # Russell 2000
ticker = "AAPL" # Individual stocks
```

## ⚠️ Disclaimer

This code is for educational and research purposes only. Past performance does not guarantee future results. Always conduct thorough testing and risk assessment before implementing any trading strategy with real money.

As when trying with different assets, you will see that the performance of buy-and-hold strategy is generally better than the breakout strategy.
## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements:
- Additional technical indicators
- More sophisticated exit strategies
- Risk management enhancements
- Performance optimization
- Bug fixes and improvements
