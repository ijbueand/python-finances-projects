import matplotlib.pyplot as plt
import pandas_datareader.data as wb

assets = 'TSLA'
data = wb.DataReader(assets, 'yahoo', '2020-1-1')

high9 = data.High.rolling(9).max()
Low9 = data.High.rolling(9).min()
high26 = data.High.rolling(26).max()
Low26 = data.High.rolling(26).min()
high52 = data.High.rolling(52).max()
Low52 = data.High.rolling(52).min()

data['tenkan_sen'] = (high9 + Low9)/2
data['kijun_sen'] = (high26 + Low26) /2
data['senkou_A'] = ((data.tenkan_sen + data.kijun_sen) /2).shift(26)
data['senkou_B'] = ((high52 + Low52)/2).shift(26)
data['chikou'] = data.Close.shift(-26)
data = data.iloc[26:]

plt.plot(data.index, data['tenkan_sen'], lw=0.7)
plt.plot(data.index, data['kijun_sen'], lw=0.7)
plt.plot(data.index, data['chikou'], lw=0.7)
plt.title("Ichimoku en :" + str(assets))
plt.ylabel("precio")
komu = data['Adj Close'].plot(lw=1.5, color='b')
komu.fill_between(data.index, data.senkou_A, data.senkou_B, where=data.senkou_A >= data.senkou_B, color='lightgreen')
komu.fill_between(data.index, data.senkou_A, data.senkou_B, where=data.senkou_A < data.senkou_B, color='lightcoral')
plt.grid()
plt.show()