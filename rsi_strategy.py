import pandas_datareader.data as wb
import yfinance as yfin
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
yfin.pdr_override()

ticker = ['IAG.MC','SAN.MC']

df = wb.get_data_yahoo(ticker, start='2020-10-1')['Adj Close']

weights = np.array([0.2,0.8])
df = (df*weights).sum(axis=1)

returns = df.pct_change()[1:]
long_window = 14
up = returns.clip(lower=0)
down = -1*returns.clip(upper=0)

ema_up = up.ewm(span=long_window).mean()
ema_down = down.ewm(span=long_window).mean()

rs = ema_up/ema_down
rsi = 100-(100/(1+rs))

signal = pd.DataFrame(index = df.index)
signal['RSI'] = rsi

signal['signalbuy'] = np.where(signal['RSI'] < 30, 1,0)
signal['positionbuy'] = signal['signalbuy'].diff()

signal['signalsell'] = np.where(signal['RSI'] > 70, 1,0)
signal['positionsell'] = signal['signalsell'].diff()

df = df.iloc[long_window:]
signal = signal.iloc[long_window:]

data = pd.DataFrame()
data['Precio'] = df
data['signal C'] = signal['positionbuy']
data['signal V'] = signal['positionsell']
data['Compra'] = 0
data['Venta'] = 0
data['I.Compra'] = 0
data['I.Venta'] = 0
data['Stock'] = 0
data['Portfolio'] = 0
data['Cash'] = 0
data['PyG'] = 0
data['Comisiones'] = 0
data = data.reset_index()

capital = 100000
orden = int(2000)
lotemin = int(10)
cashmin = int(100)
cf = int(5)
cv = 0.001
parte = 0.5

data.loc[0,'Cash']= capital 
data.loc[0,'Total']= capital

for x in range(len(data)):
    if x == 0:
        x=1
    data.loc[x, 'Cash'] = data.iloc[(x-1), 10]
    data.loc[x, 'Stock'] = data.iloc[(x-1),8]
    data.loc[x, 'Portfolio'] = data.iloc[x, 8] * data.iloc[x, 1] 
    data.loc[x,'PyG'] = data.iloc[x,10] + data.iloc[x,9]-capital  
    if (data.iloc[x, 2] == -1 and data.iloc[(x-1),10]>0):
        lote = orden 
        comfix = cf
        if (data.iloc[(x-1),10]) < (lote*data.iloc[x,1]+(cf+cv*data.iloc[x,1]*lote)+cashmin):  
            lote = (data.iloc[(x-1),10]-(cf+cv*data.iloc[x,1]*orden)-cashmin)//data.iloc[x,1]
        if (data.iloc[(x-1),10]) < (lote*data.iloc[x,1]+(cf+cv*data.iloc[x,1]*lote)):  
            lote = (data.iloc[(x-1),10]-(cf+cv*data.iloc[x,1]*orden))//data.iloc[x,1]
            if lote < lotemin:
                lote=0
                cf=0
        if data.iloc[(x-1),10] > (lote * data.iloc[x, 1]):
            data.loc[x, 'I.Compra'] =  lote * data.iloc[x, 1]
            data.loc[x, 'Compra'] = lote 
            data.loc[x, 'Stock'] = lote + data.iloc[(x-1),8]
            data.loc[x, 'Portfolio'] = data.iloc[x, 8] * data.iloc[x, 1]
            data.loc[x, 'Comisiones']= cf + cv*data.iloc[x,6]
            data.loc[x, 'Cash'] = data.iloc[(x-1),10] - data.iloc[x,6]-data.iloc[x,12]
    elif (data.iloc[x, 3] == -1 and data.iloc[(x-1),8]>0) :
        paquete = int(data.iloc[(x-1),8] * parte)
        if paquete < lotemin:
            paquete=0
            cf=0
        data.loc[x, 'I.Venta'] =  paquete * data.iloc[x, 1]
        data.loc[x, 'Venta'] = paquete 
        data.loc[x, 'Stock'] = data.iloc[(x-1),8] - paquete 
        data.loc[x, 'Portfolio'] = data.iloc[x, 8] * data.iloc[x, 1]
        data.loc[x, 'Comisiones']= cf + cv*data.iloc[x,7]
        data.loc[x, 'Cash'] = data.iloc[(x-1),10]+ data.iloc[x,7]-data.iloc[x,12]
    else:       
        data.loc[x, 'Portfolio'] = data.iloc[x, 8] * data.iloc[x, 1] 
        data.loc[x,'PyG']= data.iloc[x,10]+data.iloc[x,9]-capital     

data.set_index('Date', inplace=True) 

data['Total'] = (data['Portfolio'] + data['Cash'])
data['Returns'] = data['Total'].pct_change()[1:]
data['Returns'] = data['Returns'][data['Returns'] != 0]

print('\n Valor total neto cash + cartera al final del periodo ', round(data['Total'][-1],2))

fig = plt.figure(figsize=(16,8))
fig.suptitle(ticker)

ax1 = fig.add_subplot(221, ylabel="Precio")
ax2 = fig.add_subplot(223, ylabel="RSI")
ax3 = fig.add_subplot(222, ylabel="Valor de la cartera")
ax4 = fig.add_subplot(224, ylabel="Frecuencia")

ax1.set_title("Estrategia RSI: " + str(ticker))
ax1.get_xaxis().set_visible(False)

df.plot(ax=ax1, color='b', lw=1.1)
ax1.plot(df[signal['positionbuy'] == -1], '^', markersize=8, color='g')
ax1.plot(df[signal['positionsell'] == -1], 'v', markersize=8, color='r')

signal.RSI.plot(ax=ax2, color='b')
ax2.set_ylim(0,100)
ax2.axhline(70, color='r', linestyle='--')
ax2.axhline(30, color='r', linestyle='--')

data.Total.plot(ax=ax3, color='b', lw=1.1)
ax3.set_title("Capital: " +  str(capital) + "\nLote: " + str(orden) + "\nVentas del: " + str(parte*100) +"%")
ax3.plot(data['Total'][signal['positionbuy'] == -1], '^', markersize=8, color='g')
ax3.plot(data['Total'][signal['positionsell'] == -1], 'v', markersize=8, color='r')
sns.histplot(data['Returns'], kde=True, ax=ax4)
plt.show()