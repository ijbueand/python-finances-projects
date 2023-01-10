import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import yfinance as yfin

yfin.pdr_override()

# Evolución de los precios a lo largo del tiempo

assets = ['TLSA', 'AAPL', 'MSFT', 'IBM']

data = pd.DataFrame()

for t in assets:
    data[t] = wb.get_data_yahoo(t, start='2018-01-01')['Adj Close']

(data / data.iloc[0]*100).plot(figsize=(12,6))
plt.show()

# Creando un gráfico de velas

import plotly.graph_objects as go

def create_charts(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])])
    fig.show()

create_charts(pd.read_csv('NIO.csv'))