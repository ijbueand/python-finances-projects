import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt
from scipy.stats import norm 

r = 0.0137
K = 124
T = 1

data = pd.DataFrame()
data = wb.get_data_yahoo('META', start='2013-1-1')['Adj Close']

log_returns = np. log (1+data.pct_change ())
S = data.iloc[-1]
Vol = log_returns.std()*252**0.5

def d1(S, K, r, Vol, T):
    return (np. log(S/K) + ((r + Vol**2)/2)*T) / (Vol * np. sqrt (T))

def d2(S, K, r, Vol, T):
    return (np. log(S/K) + ((r - Vol**2)/2) *T) / (Vol * np.sqrt (T))

def BSCallGreeks(S, K, r, Vol, T):
    d_uno = d1(S, K, r, Vol, T)
    d_dos = d2(S, K, r, Vol, T)
    Delta = norm.cdf (d_uno)
    Gamma = norm.pdf (d_uno)/(S*Vol*np.sqrt(T))
    Theta = (S*Vol*norm.pdf (d_uno)) / (2*np.sqrt (T)) - r*K* (np.exp(-r*T))*norm.cdf(d_dos)
    Vega = S*np.sqrt(T)*norm.pdf(d_uno)
    Rho = K*T*(np.exp(-r*T))*norm.cdf(d_dos)
    return print('\nLas griegas de las opciones de compra: \n', 
                    '\nLa Delta es: ', Delta,
                    '\nLa Gamma es: ', Gamma,
                    '\nLa Theta es: ', Theta,
                    '\nLa Vega es: ', Vega,
                    '\nLa Rho es: ', Rho)

BSCallGreeks(S, K, r, Vol, T)