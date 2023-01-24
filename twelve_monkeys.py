'''En este programa vamos a replicar el experimento que trató de refutar la crítica 
del norteamericano Burton Gordon Malkiel en 1973, en el que afirmaba que un mono 
lanzando dardos sería capaz de tener unos retornos similares al resto de gestores.

La idea es generar aleatoriamente 12 carteras de 10 activos, ponderadas por igual, 
y calcular la rentabilidad media para el periodo.'''

import pandas as pd
import random
import yahoo_fin.stock_info as si
import matplotlib.pyplot as plt
import yfinance as yf

tickers=[]
tabla=[]
ticks=[0]*10
barras=[]
monos=pd.DataFrame(columns=['Random 1','Random 2','Random 3',
'Random 4','Random 5','Random 6','Random 7',
'Random 8','Random 9','Random 10','Rent.md.'], index=range(24))

lt = si.tickers_sp500()

for m in range(0,24,2):
    print('Mono ',m//2)
    ticks=random.sample(range(len(lt)),10)
    for i in range(10):
        tickers.append(lt[ticks[i]])
    df = yf.download(tickers,auto_adjust=False,start="2021-01-01")['Close']
    for i in range(10):
        tabla.append(round(float(df.iloc[(len(df)-1),i]/df.iloc[0,i]-1)*100,2))
        monos.iloc[m,i]=tickers[i]
        monos.iloc[(m+1),i]=tabla[i]
    tickers=[]  
    tabla=[] 

suma=float(0)

for i in range(0,24,2):
    for n in range(10):
        suma=suma+float(monos.iloc[(i+1),n]) 
    suma=round(float(suma)/10,2)
    barras.append(suma) 
    monos.iloc[i+1,10]=suma 
    monos.iloc[(i),10]=('Mono: ',i//2+1)
    suma=0

print(monos)

monos2 = []
for x in range(12):
    monos2.append("Mono/s "+str(x+1))

plt.figure(figsize=(16,8))
plt.bar(monos2, barras)
plt.title('Rentabilidad de la cartera de cada mono')
plt.ylabel('Porcentaje %')
plt.xlabel('Monos')
plt.show()