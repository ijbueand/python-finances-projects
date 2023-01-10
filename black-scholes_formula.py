import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt
from scipy.stats import norm 

r = 0.0137
K = 130
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

def BSCall(S, K, r, Vol, T):
    d_uno = d1(S, K, r, Vol, T)
    d_dos = d2(5, K, r, Vol, T)
    return (S*norm.cdf (d_uno)) - (K*np.exp(-r*T) *norm. cdf(d_dos))

def BSPut (S, K, r, Vol, T):
    d_uno = d1(S, K, r, Vol, T)
    d_dos = d2(5, K, r, Vol, T)
    return (K*np.exp(-r*T)*norm.cdf (-d_dos)) - (S*norm.cdf (-d_uno))

print("\nPrecio de la Call: \n", BSCall(S, K, r, Vol, T), "\n")
print ("\nPrecio de la Put: \n", BSPut(S, K, r, Vol, T), "\n")