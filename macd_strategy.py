'''This code implements an algorithm to trade Tesla stock based on the Moving Average Convergence 
Divergence (MACD) technical indicator. It retrieves stock data for Tesla from Yahoo Finance, 
calculates the MACD and signal line values, and generates a series of signals indicating when to 
buy (1) or sell (0). It then simulates the trade based on these signals, keeping track of the 
portfolio value and returns. Finally, it produces a graph showing the portfolio value over time and 
a histogram of the returns, as well as a graph showing the stock price, MACD and signal line values, 
and the MACD histogram.'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas_datareader.data as wb
import seaborn as sns

data = wb.DataReader('TSLA', 'yahoo', '2020-1-1', '2022-1-1')['Adj Close']

m_rap = data.ewm(span=12, adjust=False).mean()
m_lenta = data.ewm(span=26, adjust=False).mean()

macd = m_rap - m_lenta
ema9 = macd.ewm(span=9, adjust=False).mean()
histograma = macd - ema9

signal = pd.DataFrame(index=data.index)
signal['signal'] = np.where(macd > ema9,1,0)
signal['position'] = signal['signal'].diff()

capital = 100000
stocks = int(1000)

positions = stocks*signal['signal']
portfolio = positions.multiply(data)

pos_diff = positions.diff()

cash = capital - (pos_diff.multiply(data).cumsum())
total = cash + portfolio

returns = total.pct_change()[1:]
returns = returns[returns != 0]

print("\n Valor total bruto de la cartera al final del periodo:", round(total.iloc[-1],2))

fig= plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(121)
ax1.set_title("Valor bruto de la cartera con " + str(capital) + " euros y " + str(stocks) + " acciones")
total.plot(ax=ax1, lw=2.)
ax1.plot(total[signal['position'] == 1], '^', markersize=9, color='g')
ax1.plot(total[signal['position'] == -1], 'v', markersize=9, color='r')

ax2 = fig.add_subplot(122)
ax2.set_title("Frecuencia de los retornos")
sns.histplot(returns, kde=True, ax=ax2)

grafico = plt.figure(figsize=(20,10))
tabla = gridspec.GridSpec(nrows=2, ncols=1, figure=grafico, height_ratios=[3,1])

graf_sup = plt.subplot(tabla[0,0])
graf_inf = plt.subplot(tabla[1,0])

graf_sup.plot(data, label='Cierre')
graf_sup.plot(data[signal['position']== 1], '^', markersize=9, color='g')
graf_sup.plot(data[signal['position']== -1], 'v', markersize=9, color='r')
graf_sup.set_title("Precio")

graf_inf.plot(data.index, macd, 'b', label="MACD")
graf_inf.plot(data.index, ema9, 'r--', label="Signal")
graf_inf.bar(data.index, histograma, color=(histograma>0).map({True:'g', False:'r'}))
graf_inf.set_title("MACD")
plt.grid()
plt.show()