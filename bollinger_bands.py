import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt

data = wb.DataReader('TEF.MC', 'yahoo', '2017-1-1')

data['std']=data['Adj Close'].rolling(20).std()
data['MA']=data['Adj Close'].rolling(20).mean()

data['Up']= data['MA'] + 2*data['std'] 
data['Down']= data['MA'] - 2*data['std']

ax = data[['Adj Close', 'Up', 'Down']].plot(color=['blue', 'green', 'red'])
ax.fill_between(data.index, data['Down'], data['Up'], facecolor='orange', alpha=0.1) 
plt.show()