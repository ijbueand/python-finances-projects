import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt

yfin.pdr_override()

# Importamos todos los datos (date, open, high, low, close, adj close y volume) de AMAZON
ticker = 'AMZN'
data = wb.get_data_yahoo(ticker, start='2015-01-01')
data = data.reset_index()

# Calculamos el SMA y el EMA
def compute_SMA(data, window):
    sma = data.rolling(window=window).mean() 
    return sma

def compute_EMA(data, span):
    ema = data.ewm(span=span).mean()
    return ema

# Creamos el dataframe con las medias
def construct_df(ticker):
    data
    for i in range(50, 250, 50):
        data['SMA_{}'.format(i)] = compute_SMA(data['Adj Close'], i)
        data['EMA_{}'.format(i)] = compute_EMA(data['Adj Close'], i)
    return data

df = construct_df(ticker)

# Graficamos los resultados 
def plot_data_SMA(df):
    plt.figure(figsize=(16,8))
    plt.title(ticker + ' SMA')
    plt.plot(df['Date'], df['Adj Close'])

    for i in range (50, 250, 50):
        plt.plot(df['Date'], df['SMA_{}'.format(i)])
    plt.show()

def plot_data_EMA(df):
    plt.figure(figsize=(16,8))
    plt.title(ticker + ' EMA')
    plt.plot(df['Date'], df['Adj Close'])

    for i in range (50, 250, 50):
        plt.plot(df['Date'], df['EMA_{}'.format(i)])
    plt.show()

plot_data_SMA(df)
plot_data_EMA(df)