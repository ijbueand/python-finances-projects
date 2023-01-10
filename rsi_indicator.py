import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt

ticker = 'SAN.MC'
data = wb.DataReader(ticker, 'yahoo', '2018-1-1')['Adj Close']

returns = data.pct_change()
up = returns.clip(lower=0)
down = -1*returns.clip(upper=0)

ema_up = up.ewm(com=13, adjust=False).mean()
ema_down = down.ewm(com=13, adjust=False).mean()
rs = ema_up/ema_down

datarsi = 100-(100/(1+rs))

fig, (ax1, ax2) = plt.subplots(2)
ax1.get_xaxis().set_visible(False)
fig.suptitle(ticker)

data.plot(ax=ax1)
ax1.set_ylabel(ticker + ' Precio')

datarsi.plot(ax=ax2)
ax2.set_ylim(0, 100) 
ax2.set_ylabel('RSI') 
ax2.axhline(70, color='r' , linestyle='--')
ax2.axhline(30, color='r', linestyle='--')

plt.show()