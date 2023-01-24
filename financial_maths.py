### EJERCICIOS DE MATEMÁTICAS FINANCIERAS ###

#################################################################

# 1. VALOR PRESENTE Y FUTURO

'''Vamos a programar un valor final, VF, y un valor actual, VA,
igual que ser haría en Excel. Los argumentos van a ser la cuota,
el tipo de interés y el número de periodos.

El valor presente de una inversión es cuando calculamos el valor 
actual que tendrá una determinada cantidad que recibiremos o 
pagaremos en un futuro. El valor futuro es el valor alcanzado por 
un determinado capital al final del período determinado (para el 
ejemplo usaremos la fórmula del interés compuesto).

Vamos a hacerlo de una renta, con lo cual hay un cálculo recursivo
en el que cada vez que hagamos una actualización ese cálculo deberá
aplicarse otra vez la fórmula.'''

cuota = float()
interes = float()
periodo = float()
tipo = int()

def final_value(cuota, interes, periodo, tipo):
    resultado = 0.0
    for t in range(periodo):
        if tipo == 1: 
            # Si es tipo anticipada
            resultado += cuota*(1+interes)**(t+1)
        else: 
            # Si es tipo vencida
            resultado += cuota*(1+interes)**(t)
    print('El valor final es: ', round(resultado, 2))

print('\nVALOR FINAL DE UNA RENTA')
print('-------------------------\n')
cuota = float(input('Introduzca su cuota anual: '))
interes = float(input('Introduzca su tasa de interés anual: '))
periodo = int(input('Introduzca los años del periodo: '))
tipo = int(input('Introduzca 1 si es de tipo anticipada o 0 si es de tipo vencida: '))

final_value(cuota, interes, periodo, tipo)

#################################################################

# 2. EL SISTEMA DE AMORTIZACIÓN FRANCÉS

'''Se trata de obtener una cuota de amortización constante para un 
préstamo (generalmente hipotecas para este caso). Se pagan intereses 
en función del capital pendiente a amortizar, que irá decreciendo a 
medida que vayamos amortizándolo con nuestra cuota.'''

import pandas as pd
import matplotlib.pyplot as plt

print("\n"*2)
print('PRÉSTAMO SISTEMA FRANCES')

cuota = float(0)
capital = int(input('Capital : '))
tipo = float(input('T.int. anual nominal: '))
periodo = int(input('Num. pagos: '))
o = int(input('Pagos por año: '))

cuota= round(capital*((tipo/(o*100))/(1-(1+(tipo/(o*100)))**(-1*periodo))),2)
print(    'Plan de pagos')

plan = pd.DataFrame(columns=['Cuota','Interes','Amort.','Capital'])
plan.loc[0,'Capital']= capital
plan.loc[0,'Cuota']= 0
plan.loc[0,'Interes']= 0
plan.loc[0,'Amort.']= 0

for t in range(1,periodo+1):
    plan.loc[t,'Cuota']= cuota
    plan.loc[t,'Interes']= round(float(plan.loc[t-1,'Capital']*(tipo/(100*o))),2)
    plan.loc[t,'Amort.']= (plan.loc[t,'Cuota']-plan.loc[t,'Interes'])
    plan.loc[t,'Capital']= plan.loc[t-1,'Capital']-plan.loc[t,'Amort.']

print(plan)
print('\nTotal intereses :',round(float(plan['Interes'].sum()),2))

'''Para finalizar y a modo opcional, dibujamos en un gráfico la evolución 
de los intereses y la amortización pagada, relación inversa entre ambas.'''

fig = plt.figure(figsize=(16,8))
fig.suptitle('Evolución de interés y amortización')
ax1 = fig.add_subplot(ylabel='Importes', xlabel='Tiempo')
ax1.plot(plan['Interes'], ':', label = 'Interés', markersize=30, color='b', linewidth=2.0)
ax1.plot(plan['Amort.'], ':', label = 'Amortización', markersize=30, color='g', linewidth=2.0)
ax1.plot(plan['Cuota'], ':', label = 'Cuota', markersize=30, color='k', linewidth=3.0)
ax1.legend()
plt.show()

#################################################################

# 3. LA TIR NO PERIÓDICA (TIR.NO.PER)

'''Consiste en la tasa interna de retorno de una inversión en función 
de una serie especificada de flujos de efectivo que no son necesariamente 
periódicos. No existe "fórmula" como tal, y hay que hacer un cálculo 
recursivo delimitando un rango en función del número de decimales de 
precisión requeridos (2 decimales para nuestro ejemplo)'''

import numpy as np
import matplotlib.pyplot as plt

print("\n"*2)
print('CÁLCULO DE LA TIR NO PERIÓDICA (MWR)')

cf=[400,200,600,200,-1800]

year=[]
fcha=[]

fecha=['2020/01/01','2020/05/01','2021/01/01','2021/03/01','2021/05/03']

for z in range(len(fecha)):
    fcha.append(int(fecha[z][0:4])*360+int(fecha[z][5:7])*30+int(fecha[z][8:10]))

for z in range(len(fecha)):
    year.append(round(float((fcha[z])-fcha[0])/360,4))

vant=[]
van=float(0)

i=-9999
while i<10000:
    for z in range(len(cf)):
        van = van+(-cf[z]/(1+i/10000)**(year[z]))
    vant.append(np.where(van>0,1,-1))
    van=0 

if len(vant)>1:
    if vant[len(vant)-1]+vant[len(vant)-2]== 0:
        print('el TIR es: ',round(float(i)/100,2),'%')
        tir=round(float(i)/100,2)
i+=1 # sumamos 0.01% cada paso

fig = plt.figure(figsize=(20,10))
fig.suptitle('Evolución signo VAN')
ax1 = fig.add_subplot(ylabel='+1/-1')
ax1.plot(vant[1:], markersize=30, color='b')

plt.axhline(0, color='k', lw=1, linestyle='--')
plt.axvline(10000, color='k', lw=1, linestyle='--')
plt.show()