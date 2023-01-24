'''Este indicador está pensado para detectar tendencias en 
activos estacionales como las materias primas.'''

import pandas_datareader.data as wb
import matplotlib.pyplot as plt
import yfinance as yfin
yfin.pdr_override()

ticker = 'IAG.MC'
data = wb.get_data_yahoo(ticker, start='2021-1-1')

days = 14
typical_price = (data.High + data.Low + data.Close)/3
CCI = (typical_price - typical_price.rolling(days).mean())/(0.015*typical_price.rolling(days).std())
CCI = CCI[days:]

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Indicador CCI')
ax1.get_xaxis().set_visible(False)
data.Close.plot(ax=ax1, ylabel='Precio AAPL')
CCI.plot(ax=ax2, color='k', ylabel='CCI').fill_between(CCI.index, CCI, where = CCI > 0, color = 'lightgreen')
plt.show()

'''Interpretación: las zonas coloreadas en verde son zonas con tendencia fuerte, bien se alcista o bajista.'''