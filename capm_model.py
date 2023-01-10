import numpy as np
import pandas as pd
import pandas_datareader as wb
import yfinance as yfin

tickers = ['META', '^GSPC']

data = pd.DataFrame()
for t in tickers:
    data[t] = wb.get_data_yahoo(t, start='2013-1-1')['Adj Close']

# Obtenemos los retornos logarítmicos y la covarianza entre nuestros activos
log_returns = np.log(1+data.pct_change())
cov = log_returns.cov()*252

# Fijamos el dato de la covarianza con el mercado
cov_market = cov.iloc[0,1] # Covarianza del mercado con Facebook
market_var = log_returns['^GSPC'].var()*252 # Varianza del mercado 

# Obtenemos la beta (medida del riesgo de la inversión)
stock_beta = cov_market/market_var

''' El resultado es 1.105, por lo que Facebook se mueve
más que el mercado.'''

# Definimos la tasa libre de riesgo y el riesgo premium
r_free = 0.0137
r_premium = (log_returns['^GSPC'].mean()*252) - r_free

# Calculamos el CAPM
stock_capm_return = r_free + stock_beta*r_premium

# Calculamos el Sharpe
sharpe = (stock_capm_return - r_free) / (log_returns['META'].std()*252**0.5)

print('La beta de ' + str(tickers) + ' es de: ' + str(round(stock_beta, 3)))
print('El retorno CAPM de ' + str(tickers) + ' es de: ' + str(round(stock_capm_return, 3)*100) + '%')
print('El ratio de Sharpe de ' + str(tickers) + ' es de: ' + str(round(sharpe, 3)))