'''Vamos a estimar un modelo econométrico sencillo como puede
ser una regresión lineal simple a través de mínimos cuadrados.
La función de consumo es básica, con el consumo (PCEC) y el 
ingreso (GDP)'''

import pandas_datareader.data as wb
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import numpy as np

tickersfred = ['PCEC', 'GDP']
data = wb.DataReader(tickersfred, 'fred', '2010-01-01')

plt.plot(data.index, data, lw=1.5)
plt.legend(data.columns)
plt.show()

model = smf.ols('PCEC ~ GDP', np.log(data)).fit()
print(model.summary(), model.params)

plt.plot(data.index, data.diff(), lw=1.5)
plt.legend(data.columns)
plt.show()

