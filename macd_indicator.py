import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas_datareader as wb

data = wb.DataReader('NIO', 'yahoo', '2022-1-1')['Adj Close']

m_rap = data.ewm(span=12, adjust=False).mean()
m_len = data.ewm(span=26, adjust=False).mean()

macd = m_len - m_rap
signal = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal 

grafic = plt.figure(figsize=(20, 10))
tabla = gridspec.GridSpec(nrows=2, ncols=1, figure=grafic, height_ratios=[3,1])

graf_sup = plt.subplot(tabla[0,0])
graf_inf = plt.subplot(tabla[1,0])

graf_sup.plot(data, label='Cierre')
graf_sup.set_title('Precio')

graf_inf.plot(data.index, macd, 'b', label='MACD')
graf_inf.plot(data.index, signal, 'r--', label='Signal')
graf_inf.bar(data.index, histogram, color='k')

plt.grid()
plt.show()