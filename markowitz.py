''' OPTIMIZACIÓN DE CARTERAS CON MARKOWITZ

El usuario escoge una serie de acivos y nosotros le decimos el peso óptimo para cada 
activo de forma que se maximice la rentabilidad:riesgo (ratio Sharp). También se puede hacer 
minimizando la volatilidad independientemente de los retornos o maximizando los retornos 
independientemente de la volatilidad, pero nosotros elegimos maximizar la rentabilidad:riesgo.'''

import pandas as pd
import numpy as np
import pandas_datareader as wb
import yfinance as yfin
import matplotlib.pyplot as plt
import scipy.optimize as optimize

yfin.pdr_override()

'''Parte I - Generamos múltiples portafolios con pesos al azar, siempre con el 100% invertido, 
en el que calcularemos las volatilidades de cada portafolio'''

assets = ['V', 'HD', 'JD']

data = pd.DataFrame()
for t in assets:
    data[t] = wb.get_data_yahoo(t, start='2013-01-01', end='2021-03-01')['Adj Close']

# Obtenemos los retornos logarítmicos (también se puede la simple) y la covarianza entre nuestros activos
log_returns = np.log(1+data.pct_change())

port_returns = [] # Retornos del portafolio
port_vols = [] # Volatilidades del portafolio

for i in range(10000):
    num_assets = len(assets) # Número de activos que tenemos en assets
    weights = np.random.random(num_assets) # Para cada activo, se elgie un valor flotante del 0 al 1
    weights /= np.sum(weights) # Hacemos que entre todos sumen uno
    port_returns.append(np.sum(weights*log_returns.mean())*252) # Suma en asignación a la variable port_returns en la que hacemos la suma ponderada por los pesos y la media logarítmica anualizada
    port_vols.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov()*252, weights)))) # Calculamos las volatilidades del portafolio

# Pasamos las variables de lista a matriz
port_returns = np.array(port_returns)
port_vols = np.array(port_vols)

# Definimos una función que empaquete todo
def portfolio_stats(weights, log_returns):
    port_returns = np.sum(weights*log_returns.mean())*252 
    port_vols = np.sqrt(np.dot(weights.T, np.dot(log_returns.cov()*252, weights)))
    sharpe = port_returns/port_vols
    return {'Return': port_returns, 'Volatility': port_vols, 'Sharpe': sharpe}

'''Parte II - Maximizamos el ratio Sharp, lo mostramos por pantalla y lo graficamos'''
sharpe = port_returns/port_vols
max_sr_returns = port_returns[sharpe.argmax()]
max_sr_volatility = port_vols[sharpe.argmax()]

print('max_sr_returns = ', max_sr_returns)
print('max_sr_volatility = ', max_sr_volatility)

# Función que minimice las variables para tener el ratio sharp aislado
def minimize_sharpe(weights, log_returns):
    return -portfolio_stats(weights, log_returns)['Sharpe']

# Hay tres variables que hay que pasar como argumento a la siguiente función de optimización
initializer = num_assets * [1./num_assets,] 
bounds = tuple((0, 1) for x in range(num_assets))

# Para asegurarnos de que los pesos sumen uno
def sum_to_one(weights):
    return np.sum(weights) - 1

constraints = [
    {'type': 'eq', 'fun': sum_to_one}
]

optimal_sharpe = optimize.minimize(minimize_sharpe, initializer, method = 'SLSQP', args = log_returns, bounds = bounds, constraints=constraints)
optimal_sharpe_weights = optimal_sharpe['x'].round(3)
optimal_stats = portfolio_stats(optimal_sharpe_weights, log_returns)

print("Pesos óptimos de la cartera: ", list(zip(assets, list (optimal_sharpe_weights*100))))
print ("Retorno óptimo de la cartera: ", np.round(optimal_stats['Return']*100,3))
print("Volatilidad óptima de la cartera: ", np.round(optimal_stats['Volatility']*100,3)) 
print("Sharpe óptimo de la cartera: ", np.round(optimal_stats['Sharpe'], 3))

plt.figure(figsize=(16,6))
plt.scatter(port_vols, port_returns, c=(port_returns/port_vols))
plt.scatter(max_sr_volatility, max_sr_returns, c='red', s=30)
plt.colorbar(label='Sharpe Ratio, rf=0')
plt.xlabel('Volatilidad de la Cartera')
plt.ylabel('Retornos de la Cartera')
plt.show()
