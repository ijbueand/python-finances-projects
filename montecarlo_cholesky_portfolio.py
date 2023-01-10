''' En el primer proyecto de Monte Carlo, tratábamos de determinar el precio
de un activo a futuro con un número de pruebas y un número de días determinado.

Ahora vamos a hacer lo mismo para una cartera de tamaño determinado, con unos 
activos y unos pesos para cada activo determinados (podemos usar el proyecto
de Markowitz para obtener los pesos óptimos). 

Esto lo vamos a hacer a partir de la descomposición de Cholesky, que en el 
método de Monte Carlo se utiliza para simular sistemas con variables múltiples 
correlacionadas. Lo que se hace es descomponer esta matriz, obtener la triangular 
inferior (L) y multiplicar por el vector u (variables numéricas aleatorias 
distribuidas de forma normal) para generar el vector Lu, que mantiene las 
propiedades de covarianza del sistema para su consiguiente modelización.'''

# Importamos las librerías que vamos a necesitar
import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm 
import yfinance as yfin

yfin.pdr_override()

'''En la primera parte del código se definen las variables que se utilizarán 
en la simulación. En particular, se especifican los tickers de los valores que 
forman parte de la cartera, los pesos de cada uno de ellos en la cartera, el 
número de días a simular y el dinero invertido en la cartera. Luego, se importan 
los datos de cierre ajustado de cada valor desde Yahoo Finances y se calculan 
algunas medidas estadísticas como la media, la varianza y la desviación estándar 
de los rendimientos diarios.'''

# Definimos nuestra cartera con sus pesos (optimizados por Markowitz)
tickers = ['META', 'AAPL', 'MSFT', 'IBM', 'TSLA']
num_stocks = len(tickers)
weights = [0.123, 0.124, 0.505, 0.00, 0.248]

# Importamos los datos de Yahoo Finances
data = pd.DataFrame()
for t in tickers:
    data[t] = wb.get_data_yahoo(t, start='2015-01-01')['Adj Close']
logr = np.log(1+data.pct_change()[1:])

m = logr.mean() # Media
var = logr.var() # Varianza
drift = m-(0.5*var) # Drift
covar = logr.cov() # Covarianza
stdev = logr.std() # Desviación Estándar

trials = 10000 # Número de pruebas
days = 1000 # Número de días

simulaciones = np.full(shape=(days, trials), fill_value=0.0) # Matriz de tamaño días x trials

cartera = float(500000) # El dinero invertido en nuestra cartera

'''En la segunda parte del código se utiliza la descomposición de Cholesky para obtener 
una matriz chol que mantiene las propiedades de covarianza de los rendimientos diarios. 
Luego, se utiliza un vector de ruído aleatorio u para obtener una matriz Lu que también 
mantiene las propiedades de covarianza.'''

chol = np.linalg.cholesky(covar) # Obtenemos la triangular inferior (L)
u = norm.ppf(np.random.rand(num_stocks, num_stocks)) # Obtenemos el vector de ruído aleatorio (u)
Lu = chol.dot(u) # Multiplicamos las dos matrices para obtener la matriz Lu

'''En la tercera parte del código se inicia un bucle que se repite un número determinado 
de veces (trials) y que simula el rendimiento diario de la cartera durante un número 
determinado de días (days). Para cada iteración del bucle, se calculan los rendimientos 
diarios de cada valor de la cartera utilizando la matriz Lu, la media y la desviación 
estándar de los rendimientos diarios, y los pesos de cada valor en la cartera. Luego, 
se acumulan los rendimientos diarios para cada día en una matriz simulaciones, que al 
final del bucle tendrá el rendimiento acumulado de la cartera en cada día de la simulación.'''

# Ya podemos empezar con el bucle de Monte Carlo
for i in range(0, trials):
    z = norm.ppf(np.random.rand(days, num_stocks))
    retornos_diarios = np.inner(Lu, drift.values + stdev.values*z)
    simulaciones[:,i] = np.cumprod(np.inner(weights, retornos_diarios.T)+1)*cartera
    simulaciones[0] = cartera

plt.figure(figsize=(15, 8))
plt.plot(simulaciones)
plt.ylabel('Valor de la Cartera')
plt.xlabel('Días')
plt.title('Simulación de Monte Carlo para ' + str(cartera) + '€\n' + str(list(zip(tickers, weights*100))))
plt.show()

sns.displot(pd.DataFrame(simulaciones).iloc[-1])
plt.ylabel('Frecuencia')
plt.xlabel('Cartera')
plt.show()