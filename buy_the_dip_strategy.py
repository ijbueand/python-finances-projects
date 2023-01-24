import pandas_datareader.data as wb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yfin
yfin.pdr_override()

porcen = 95      #(1-porcen) = % de caída.
ticker = 'META'
df = wb.get_data_yahoo(ticker, start='2020-04-01', end='2021-01-01')['Adj Close']

signal = pd.DataFrame(index = df.index)     
signal['cotdia'] = df                       # 0
signal['maximo_acumulado'] = df.cummax()    # 1
signal['compra']=(df.cummax()*porcen/100)   # 2
signal['maximos']=0                         # 3
signal['signalbuy']=0                       # 4

listmax=[] 
listcom=[] 

car = pd.DataFrame(0,index=np.arange(3),columns=['Condición','Info','Precios'])
car

k=1
while k<len(df):
    if signal.iloc[k,1] > signal.iloc[(k-1),1]:
        car.iloc[1,0]=1
        print('Registro:',k,'   **  Nuevo máximo: ', signal.iloc[k,1])
        listmax.extend([k])
    if car.iloc[1,0]==1 and signal.iloc[k,0] <= signal.iloc[k,2]:
        car.iloc[1,0] = 0
        listcom.extend([k])
        print('\nRegistro:', k,' Compramos a: ',signal.iloc[k,2],'     *\n')
    k+=1

car.iloc[0,0]= ticker
car.iloc[0,1]='MÁXIMO ABSOLUTO'
car.iloc[1,1]='ÚLTIMO PRECIO'
car.iloc[2,0]= str(100-porcen)+'%'
car.iloc[2,1]='ÚLTIMA COMPRA' 
car.iloc[2,2]= round(signal.iloc[len(df)-1,2],4)
car.iloc[1,2]= round(signal.iloc[len(df)-1,0],4)
car.iloc[0,2]= round(signal.iloc[len(df)-1,1],4)
if car.iloc[1,0]==0:
    car.iloc[1,0]='Pdt.Mx.'
else:
    car.iloc[1,0]='Pdt.Cp.'

print(car,"\n")

listmaxOK=[]

z=int(0)
k=int(0)
p=int(0)

for z in range(len(listcom)):
    while p < (len(listmax)) :
        if listmax[p] >  listcom[z]:
            mx=int(listmax[p-1])
            listmaxOK.extend([mx]) 
            break
        p+=1
    p-=1
if p<len(listmax):
    mx=int(listmax[len(listmax)-1])
    listmaxOK.extend([mx])

print("Condición de compra realizada a:")
for z in range(len(listcom)):
    print(listcom[z],round(signal.iloc[listcom[z],2],3))

print("\nMáximos que han tenido una caída del porcentaje buscado:")
for x in range(len(listmaxOK)):
    print(listmaxOK[x],round(signal.iloc[listmaxOK[x],1],3))

for i in range(len(listcom)):
    signal.iloc[listcom[i],4] = 1

for i in range(len(listmaxOK)):
    signal.iloc[listmaxOK[i],3]= 1 


print('\n'*2)
print('RESULTADO ESTRATEGIA')

inv=int(1000)
patri = pd.DataFrame(0,index=np.arange(len(listcom)),columns=['Acciones','Inversión','Valor último'])
for j in range (len(listcom)):
    patri.iloc[j,1]= int(inv)
    patri.iloc[j,0]= int(inv//signal.iloc[listcom[j],0])
    patri.iloc[j,2]= round(patri.iloc[j,0]*signal.iloc[(len(signal)-1),2],2)
    j+=1

print(patri)
print('\nInv. total:', patri['Inversión'].sum(), '\nValor actual:', patri ['Valor último'].sum())
print('Ganancia / Pérdida:' ,round((patri['Valor último'].sum()-patri['Inversión'].sum()),2) ,'\nRendimiento:', round(((patri['Valor último'].sum()/patri['Inversión'].sum())-1)*100,2), '%')

fig = plt.figure(figsize=(20,10))
fig.suptitle('Evolución de la cotización con estrategia "Buy the Dip"\n' + str(100-porcen) +' %' + " de caída\n\n" + ticker)
ax1 = fig.add_subplot( 111, ylabel='Cotización', xlabel="Fechas")

ax1.plot(df[signal['maximos'] == 1],'v', markersize=12, color='r')
ax1.plot(df[signal['signalbuy'] == 1],'^', markersize=12, color='g')

ax1.plot(df, color='k', label=ticker, lw=2)
ax1.legend()
ax1.grid()

plt.yscale('log')
plt.show()