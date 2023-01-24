import yahoo_fin.stock_info as si
import ffn
import pandas as pd
import yfinance as yfin
yfin.pdr_override()

dow = si.tickers_dow()
sp500 = si.tickers_sp500()

faang = ['META', 'AAPL', 'AMZN', 'GOOG', 'NFLX']

data = ffn.get(faang, start='2018-01-01')

perf = data.calc_stats()
perf.display()

perf = pd.DataFrame(perf.stats).T

perf[perf['avg_drawdown_days'] > 30]

