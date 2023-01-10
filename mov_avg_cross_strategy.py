'''This code is implementing a moving average crossover strategy to trade a single asset, 
Meta Platforms, Inc. (META), formerly named Facebook, Inc. The strategy generates a buy 
signal when the 50-day moving average (short window) crosses above the 150-day moving average 
(long window). Conversely, the strategy generates a sell signal when the 50-day moving average 
crosses below the 150-day moving average. The code also creates a DataFrame to keep track of 
the positions in the asset, calculates the value of the portfolio over time, and plots the 
returns distribution.'''

import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as wb
import yfinance as yfin
import numpy as np
import seaborn as sns

yfin.pdr_override()

'''This part defines the asset to trade as well as the time period for which to get the data.'''

assets = ['META']
data = wb.get_data_yahoo(assets, start='2018-01-01')['Adj Close']

'''This part defines the two moving average windows, short_window and long_window, as well as 
a DataFrame signal to store the generated signals. It then calculates the moving averages using 
these windows and stores them in the short and long columns of the signal DataFrame.'''

short_window = 50
long_window = 150

signal = pd.DataFrame(index=data.index)

signal['short']= data.rolling(short_window).mean()
signal['long']= data.rolling(long_window).mean()

# signal['ewm_short']= data.ewm(short_window).mean()
# signal['ewm_long']= data.ewm(long_window).mean()

'''This part generates the actual buy and sell signals based on the moving average crossover 
strategy. It uses NumPy's where function to create a new column in the signal DataFrame called 
signals, which is 1 when the short moving average is greater than the long moving average and 
0 otherwise.'''

signal['signals'] = np.where(signal['short'] > signal['long'], 1, 0)
# signal['signals'] = np.where(signal['ewm_short'] > signal['ewm_long'], 1, 0)

'''This part calculates the position of the portfolio at each point in time by taking the 
difference of the signals column. It stores the resulting position in a new column called positions.'''

signal['positions'] = signal['signals'].diff()

'''This part creates the first plot, which shows the asset's adjusted close price, the two 
moving averages, and the buy and sell signals.'''

fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(121, ylabel=assets)
ax1.set_title("Estrategia cruce de medias con: " + str(assets))

data.plot(ax=ax1, color='k', lw=1.9)
signal[['short', 'long']].plot(ax=ax1, lw=1.2)

ax1.plot(signal['short'][signal['positions'] == 1], '^', markersize=8, color='g')
ax1.plot(signal['short'][signal['positions'] == -1], 'v', markersize=8, color='r')

'''This part defines the initial capital and the number of stocks to hold and creates 
a DataFrame positions to store the number of stocks held at each point in time. It then 
calculates the value of the portfolio at each point in time by multiplying the number of 
stocks held by the asset's adjusted close price.'''

capital = int(100000)
stocks = int(300)

positions = pd.DataFrame(index = signal.index)
positions['META'] = stocks*signal['signals']

pos_diff = positions.diff()

port = positions['META'].multiply(data)

'''This part calculates the difference in positions between each point in time and multiplies 
it by the asset's adjusted close price to get the cash flow at each point in time. It then 
calculates the total cash in the portfolio by cumulatively summing the cash flow and stores it 
in a new column called Cash. It also calculates the total value of the portfolio by adding the 
cash to the value of the stocks held and stores it in a new column called total. Finally, it 
calculates the returns of the portfolio by taking the percentage change of the total column and 
stores it in a new column called Returns.'''

pos_diff = positions.diff()

portfolio = pd.DataFrame()

portfolio['Cartera'] = port
portfolio['Cash'] = capital - (pos_diff['META'].multiply(data).cumsum())
portfolio['total'] = portfolio['Cash'] + portfolio['Cartera']

portfolio['Returns'] = portfolio['total'].pct_change()[1:]
portfolio['Returns'] = portfolio['Returns'][portfolio['Returns'] != 0]

'''This part creates the second plot, which shows the evolution of the total value of 
the portfolio over time. It also plots the buy and sell signals.'''

ax2= fig.add_subplot(222, ylabel='Valor de la cartera')
ax2.set_title('Evolución del valor de la cartera')
portfolio['total'].plot(ax=ax2, lw=2., label="Total de la cartera")
ax2.plot(portfolio['total'][signal['positions'] == 1], '^', markersize=8, color='g')
ax2.plot(portfolio['total'][signal['positions'] == -1], 'v', markersize=8, color='r')

'''This part creates the third plot, which shows the distribution of the portfolio returns.'''

ax3= fig.add_subplot(224)
ax3.set_title('Distribución de los retornos de la cartera')
fig.subplots_adjust(hspace=0.5)
sns.histplot(portfolio['Returns'], kde=True, ax=ax3)
plt.show()