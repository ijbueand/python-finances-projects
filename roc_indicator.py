'''El indicador ROC compara el precio de cierre actual con uno
anterior a nuestro elección. Está dentro del grupo de indicadores
de momentum para identificar aceleraciones o deceleraciones en base
a un número determinado de periodos a nuestra elección'''

import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt
yfin.pdr_override()

ticker = 'IAG.MC'
data = wb.get_data_yahoo(ticker, start='2021-01-01')

N = 5
ROC = ((data.Close - data.Close.shift(N)) / data.Close.shift(N))*100
ROC = ROC[N:]

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle(str(ticker))
ax1.get_xaxis().set_visible(False)
data.Close.plot(ax=ax1, ylabel='Precio')
ROC.plot(ax=ax2, color='k', ylabel='ROC')
plt.show()