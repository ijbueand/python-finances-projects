# Importamos las librerías que vamos a necesitar
import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm 
import yfinance as yfin

# Procedemos a la descarga del precio ajustado de los precios de cierre
tickers = ['MSFT','UNP','META','IBM']
weights = [0.662, 0.123, 0.214, 0.0]
data = wb.get_data_yahoo(tickers, start='2021-01-01', end='2022-01-01')['Adj Close']

# A continuación calculamos los retornos simples y logarítmicos
returns = data.pct_change()[1:]
log_returns = np.log(1+data.pct_change())[1:]

yearly_mean = log_returns.mean()*252
yearly_cov = log_returns.cov()*252
corr_matrix = log_returns.corr()

print('\nMedia de los retornos logarítmicos: \n' + str(yearly_mean) + '\n')
print('\nMatriz de Covarianzas: \n' + str(yearly_cov) + '\n')
print('\nMatriz de Correlaciones: \n' + str(corr_matrix) + '\n')

# Una vez disponemos de los retornos, podemos calcular el retorno acumulado
# Es exactamente el mismo proceso que si dividimos cada activo por su precio inicial
cummulative_r = (1+returns).cumprod()
cummulative_r.fillna(1, inplace = True)

cummulative_r.plot()
plt.ylabel('Cumulative Returns')
plt.show()

# Ahora vamos a ver el Compound Annual Growth Rate
cagr = cummulative_r**(252/len(cummulative_r))-1
cagr.plot()
plt.show()

# Compound Annual Growth Rate ponderado por la variable pesos (weights)
portfolio_cagr = np.dot(cagr.iloc[-1], weights)
print(portfolio_cagr)

# A continuación, vamos a añadir una variable a data que sea el valor ponderado de nuestro portafolio
returns['W'] = returns.dot(weights)
cummulative_r = (1+returns).cumprod()
cummulative_r.fillna(1, inplace = True)
portafolio_cummulative_returns = cummulative_r['W']
portafolio_cummulative_returns.plot()
plt.title('Compound Annual Growth Rate')
plt.ylabel('Cumulative Returns')
plt.show()

# Vamos a ver el Drawdown del portafolio
maxr = portafolio_cummulative_returns.cummax()
drawdown = (portafolio_cummulative_returns - maxr) / maxr

ddmax = drawdown.min()
drawdown.plot()
plt.title('Drawdown del Portafolio\n DDmax: ' + str(round(ddmax*100, 3)) + '%')
plt.show()

# Podemos también realizar una media móvil (simple) y desviación estándar para periodos específicos 
period = 30
MAvrg = data.rolling(period).mean().iloc[period:]
Mstd = returns.rolling(period).std().iloc[period:]

plt.plot(data.index,data,MAvrg)
Mstd.plot()
plt.ylabel('Precio')
plt.show()

# A continuación, hacemos el spread de volatilidad
period = 20
vol = returns.rolling(period).std() * np.sqrt(period)
vol = vol.iloc[period:]

vol.plot(figsize=(10,8))
plt.title('Spread de Volatilidad')
plt.ylabel('Volatilidad')
plt.show()
