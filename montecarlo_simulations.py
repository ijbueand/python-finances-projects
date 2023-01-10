import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
from scipy.stats import norm 

''' This code generates a montecarlo simulation of the evolution of stock 
prices over a period of 100 days for a single company. The aim is to predict
the future price of an asset. '''

yfin.pdr_override()
style.use('seaborn')

# The stock prices are obtained from Yahoo Finance 

ticker = 'IAG'
data = pd.DataFrame()
data[ticker] = wb.get_data_yahoo(ticker, start='2012-01-01')['Adj Close']

''' The log returns of the stock prices are calculated using the pct_change() 
method of the DataFrame containing the stock prices and then converted to 
logarithmic form using the log() function. The mean and variance of these 
log returns are then calculated, and used to determine the drift of the process. '''

log_returns = np.log(1+data.pct_change())
u = log_returns.mean()
var = log_returns.var()
drift = u - (0.5*var)
stdev = log_returns.std()

days = 100
trials = 1000 

''' Next, 1000 trials of the evolution of the stock prices over 100 days are 
simulated. For each trial, an array of random variables is generated using the 
norm.ppf() function from the scipy.stats library. These random variables are 
used to determine the daily returns of the stock over the 100-day period, and 
these returns are used to evolve the stock prices according to a geometric 
Brownian motion process. '''

z = norm.ppf(np.random.rand(days, trials)) 
retornos_diarios = np.exp(drift.values + stdev.values * z)
camino_de_precios = np.zeros_like(retornos_diarios)
camino_de_precios[0] = data.iloc[-1]

for t in range(1, days):
    camino_de_precios[t] = camino_de_precios[t-1]*retornos_diarios[t]

''' Finally, the simulated stock prices are plotted and the distribution of 
the final simulated stock prices is plotted as a histogram. '''

plt.figure(figsize=(15,6))
plt.plot(pd.DataFrame(camino_de_precios))
plt.xlabel('Number of days')
plt.ylabel('Price of ' + ticker)
plt.show()

plt.figure(figsize=(15,6))
sns.distplot(pd.DataFrame(camino_de_precios).iloc[-1])
plt.xlabel('Price as of ' + str(days) + ' days')
plt.ylabel('Frequency')
plt.show()