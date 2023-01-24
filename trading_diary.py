'''Para el funcionamiento del programa es necesario descargar el siguiente archivo que almacena
los nombres de los tickers de Yahoo Finance: https://shorturl.at/iEMQX'''

import pandas as pd
import datetime
from csv import reader

ct=int(0)
vent=float(0)
r=int(0)
tg=int(0)
g=int(0)

coste=float(0)
print('Crear (C) / continuar (c), CARTERA : ', end="")
reg=input() 
 
if reg == 'C' or reg == 'c': 
    if reg == 'c':
        try:
            car = pd.read_csv('Cartera.csv' ,header= None)
        except FileNotFoundError:
            print('\nEl fichero no existe, créelo\n')
            exit()
        car.rename(columns={0:'Fecha', 1:'Ticker', 2: 'Cantidad',3:'Coste',4:'Venta'}, inplace=True)
        ct = len(car)
        print(ct)
        print(car)
    if reg =='C':
        print('\n¿Estás seguro de querer borrar todo? Repite entrada (C) :', end="") 
        reg = input() 
        if reg != 'C':
            exit()
        car = pd.DataFrame()
else:
    print('\nNi C, ni c : ==> Exit')
    quit()

try:
    with open('yahoospain.csv','r') as csv_file:
        csv_reader = reader(csv_file)
        [listyahoo] = list(csv_reader)

except FileNotFoundError:
    print('\nFalta fichero Yahoospain.csv')
    exit()

while True:
    try:
        print('\n** Registro libre', ct ,'o registro a modificar (entero positivo) // Intro, SALIR: ', end="",)
        r = int(input())
        if r < 0 :
            r = r*-1
            print('\nDebes introducir un número positivo, lo cambio a',r)
        if r > ct:
            print('\nHay libres menores, corrijo a',ct)
            r = ct
    except:
        break
    try:
        print('\nTicker:', end="")
        cia = input()
        cia = cia.upper()
        print(cia)
        x = cia in listyahoo
        if x == False:
            print('Aviso: NO en lista Yahoo')

        fecha = input("\nFecha Operación, dd-mm-aaaa: ")
        contfecha= datetime.datetime.strptime(fecha, "%d-%m-%Y")

        print('\nTítulos: ', end="")
        tit = int(input())
        if tit < 0:
            print('\nEs una venta, para el resto de entradas el programa tratará el signo')
            y = cia in car['Ticker'].values
            if y == False:
                print('\nEl valor no se encuentra en cartera, no puedes venderlo') 
                quit()  
            while g < ct:
                if cia == car.iloc[g,1]: #Columna "Ticker" para el registro "g"
                    tg = tg+car.iloc[g,2] #Columna "Cantidad" para el registro "g"
                g+=1
            if tg < tit * -1:
                print('\nNo tienes suficientes títulos para vender')
                quit()

        print('\nCoste: ', end="")
        cost = float(input())
        if (tit<0 and cost >0):
            cost = cost*-1

        coste = round(cost,2)
        print(coste)
        if tit < 0:
            print('\nImporte Venta ', end="")
            vent = float(input())
            if vent < 0:
                vent = vent*-1
                vent = round(vent,2)
    except:
        print('\nEntrada incorrecta , repita\n')

    else:
        car.loc[r,'Fecha'] =  fecha
        car.loc[r,'Ticker'] = cia 
        car.loc[r,'Cantidad'] = tit
        car.loc[r,'Coste']  =  coste
        car.loc[r,'Venta'] = vent
        if r == ct:
            ct+=1

if ct> 0:
    resumen = (car.groupby('Ticker').sum()) 
    resumen.insert(3,'Coste Medio ',(resumen['Coste']/resumen['Cantidad']))
    print('\n', resumen)
    car.to_csv('Cartera.csv', header=None, index= False)  
    print ('\nGrabado') 
exit()