import backtrader as bt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class BreakoutStrategy(bt.Strategy):
    """
    Simple breakout strategy that buys when price breaks above recent highs
    and sells when it breaks below recent lows
    """
    params = dict(
        lookback_period = 20,  # Number of periods to look back for high/low
        stop_loss = 0.05,      # 5% stop loss
        take_profit = 0.15,    # 15% take profit
    )
    
    def __init__(self):
        # Calculate rolling highs and lows
        self.highest = bt.indicators.Highest(self.data.high, period=self.params.lookback_period) # type: ignore
        self.lowest = bt.indicators.Lowest(self.data.low, period=self.params.lookback_period)  # type: ignore
        
        # Track entry price for stop loss/take profit
        self.entry_price = None
        self.trade_count = 0
    def next(self):
        current_price = self.data.close[0]
        
        if not self.position:  # Not in position
            # Buy signal: price breaks above recent high
            if current_price > self.highest[-1]:  # [-1] is previous period's high
                self.buy(size=int(self.broker.cash / current_price * 0.95))  # Use 95% of available cash
                self.entry_price = current_price
                self.trade_count += 1
                print(f'BUY at {current_price:.2f} on {self.data.datetime.date(0)}')
                
        else:  # In position
            # Exit conditions
            exit_signal = False
            exit_reason = ""
            
            # Sell signal: price breaks below recent low
            if current_price < self.lowest[-1]:
                exit_signal = True
                exit_reason = "Breakout Exit"
                
            # Stop loss
            elif current_price < self.entry_price * (1 - self.params.stop_loss): # type: ignore
                exit_signal = True
                exit_reason = "Stop Loss"
                
            # Take profit
            elif current_price > self.entry_price * (1 + self.params.take_profit): # type: ignore
                exit_signal = True
                exit_reason = "Take Profit"
            
            if exit_signal:
                self.sell(size=self.position.size)  # Sell all shares
                pnl = (current_price - self.entry_price) / self.entry_price * 100
                print(f'SELL at {current_price:.2f} on {self.data.datetime.date(0)} - {exit_reason} - P&L: {pnl:.2f}%')
                self.entry_price = None

class BuyHoldStrategy(bt.Strategy):
    """
    Simple buy and hold strategy for comparison
    """
    def __init__(self):
        self.bought = False
        
    def next(self):
        if not self.bought and len(self.data) == 1:  # Buy on first day
            self.buy(size=int(self.broker.cash / self.data.close[0] * 0.95))
            self.bought = True
            print(f'BUY AND HOLD at {self.data.close[0]:.2f} on {self.data.datetime.date(0)}')

def run_backtest() :
    # Download S&P 500 data
    print("Downloading S&P 500 data...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)  # 2 years of data
    
    # Download data using yfinance
    ticker = "SPY"  # SPDR S&P 500 ETF
    data : pd.DataFrame | None = yf.download(ticker, start=start_date, end=end_date)
    if data is None :
        print("Failed to download data. Please check your internet connection or the ticker symbol.")
        return
    # Preprocess data
    data = data.droplevel(-1, axis=1)  # Drop multi-index level
    #dropna 
    # data = data.dropna()  # Drop rows with NaN values
    # data = data.reset_index()  # Reset index to have 'Date' as a column
    # data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is datetime type
    # data.set_index('Date', inplace=True)  # Set 'Date' as index
    
    # Convert to backtrader format
    bt_data = bt.feeds.PandasData(dataname=data)  # type: ignore
        
    # Run breakout strategy
    print("\n" + "="*50)
    print("RUNNING BREAKOUT STRATEGY")
    print("="*50)
    
    cerebro1 = bt.Cerebro()
    cerebro1.adddata(bt_data)
    cerebro1.addstrategy(BreakoutStrategy)
    cerebro1.broker.setcash(100000.0)  # Start with $100,000
    cerebro1.broker.setcommission(commission=0.001)  # 0.1% commission
    
    # Add analyzers
    cerebro1.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro1.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro1.addanalyzer(bt.analyzers.Returns, _name='returns')
    
    starting_value1 = cerebro1.broker.getvalue()
    results1 = cerebro1.run()
    final_value1 = cerebro1.broker.getvalue()
    
    # Run buy and hold strategy
    print("\n" + "="*50)
    print("RUNNING BUY AND HOLD STRATEGY")
    print("="*50)
    
    cerebro2 = bt.Cerebro()
    cerebro2.adddata(bt_data)
    cerebro2.addstrategy(BuyHoldStrategy)
    cerebro2.broker.setcash(100000.0)
    cerebro2.broker.setcommission(commission=0.001)
    
    # Add analyzers
    cerebro2.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro2.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro2.addanalyzer(bt.analyzers.Returns, _name='returns')
    
    starting_value2 = cerebro2.broker.getvalue()
    results2 = cerebro2.run()
    final_value2 = cerebro2.broker.getvalue()
    
    # Print results
    print("\n" + "="*50)
    print("BACKTEST RESULTS COMPARISON")
    print("="*50)
    
    breakout_return = (final_value1 - starting_value1) / starting_value1 * 100
    buyhold_return = (final_value2 - starting_value2) / starting_value2 * 100
    
    print(f"\nBREAKOUT STRATEGY:")
    print(f"Starting Portfolio Value: ${starting_value1:,.2f}")
    print(f"Final Portfolio Value: ${final_value1:,.2f}")
    print(f"Total Return: {breakout_return:.2f}%")
    
    # Get analyzer results for breakout
    strat1 = results1[0]
    if hasattr(strat1.analyzers.sharpe, 'get_analysis'):
        sharpe1 = strat1.analyzers.sharpe.get_analysis().get('sharperatio', 'N/A')
        print(f"Sharpe Ratio: {sharpe1 if sharpe1 != 'N/A' else 'N/A'}")
    
    drawdown1 = strat1.analyzers.drawdown.get_analysis()
    print(f"Max Drawdown: {drawdown1['max']['drawdown']:.2f}%")
    
    print(f"\nBUY AND HOLD STRATEGY:")
    print(f"Starting Portfolio Value: ${starting_value2:,.2f}")
    print(f"Final Portfolio Value: ${final_value2:,.2f}")
    print(f"Total Return: {buyhold_return:.2f}%")
    
    # Get analyzer results for buy and hold
    strat2 = results2[0]
    if hasattr(strat2.analyzers.sharpe, 'get_analysis'):
        sharpe2 = strat2.analyzers.sharpe.get_analysis().get('sharperatio', 'N/A')
        print(f"Sharpe Ratio: {sharpe2 if sharpe2 != 'N/A' else 'N/A'}")
    
    drawdown2 = strat2.analyzers.drawdown.get_analysis()
    print(f"Max Drawdown: {drawdown2['max']['drawdown']:.2f}%")
    
    print(f"\nPERFORMANCE DIFFERENCE:")
    print(f"Breakout vs Buy&Hold: {breakout_return - buyhold_return:.2f}% difference")
    
    # # Create plots
    #fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # # Plot 1: Breakout Strategy
    cerebro1.plot(style='candlestick', barup='green', bardown='red')
    
    
    # # Plot 2: Buy and Hold Strategy  
    cerebro2.plot(style='candlestick', barup='green', bardown='red')

    
    return results1, results2

if __name__ == "__main__":
    # Run the backtest
    results = run_backtest()
    if results is not None:
        breakout_results, buyhold_results = results
    else:
        print("Backtest did not return results.")