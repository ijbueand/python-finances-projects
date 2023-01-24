import pandas as pd
import pandas_datareader.data as wb
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

S = wb.DataReader('AAPL', 'yahoo')['Adj Close'][-1] # Pasamos el último valor del subyacente

# Nos descargamos la información que ofrece yfinance sobre esta acción

aapl = yf.Ticker('AAPL')
aapl.options
opt = aapl.option_chain('2023-02-03')

# Creamos un dataframe sólo con las calls
df = pd.DataFrame(opt.calls)

# Imprimimos por ejemplo aquellos con mayor volumen acumulado
print(df[(df['openInterest'] > 10000) & (df['volume'] > 1000)])

# A continuación vamos a graficar las opciones
strike_calls = 130
strike_puts = 150
premium_c = 3
premium_p = 2

c_exp = np.arange(0.95*S, 1.10*S, 1) # Call a expiración
p_exp = np.arange(0.85*S, 1.00*S, 1) # Put a expiración

'''Lo que necesitamos ahora es hacer la condición a partir de la cual, cuando pagamos la prima
estamos en pérdidas y a partir de un cierto valor a expiración del subyacente, sobrepasando el
strike en las calls ganaríamos dinero y al revés con las puts.'''

long_call = np.where(c_exp > strike_calls, c_exp - strike_calls, 0)  - premium_c
long_put = np.where(p_exp < strike_calls, strike_puts - p_exp, 0)  - premium_p
short_call = -long_call
short_put = -long_put

fig, ax = plt.subplots()
ax.plot(p_exp, long_put, color='r')
plt.title('Long Put')
plt.xlabel('Precio a Vencimiento')
plt.ylabel('P&L')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position('zero')
plt.show()

fig, ax = plt.subplots()
ax.plot(c_exp, long_call, color='r')
plt.title('Long Call')
plt.xlabel('Precio a Vencimiento')
plt.ylabel('P&L')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position('zero')
plt.show()

