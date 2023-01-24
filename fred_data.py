'''Vamos a graficar la tasa de desempleo y compararlo en 
términos relativos por etnia, edad y nivel educativo'''

import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as wb

tickersfred = ['UNRATE', 'LNS14000003', 'LNS14000006', 'LNS14000009', 'LNU04032183']
data = wb.DataReader(tickersfred, 'fred', '2010-01-01')
data.columns = ['Unemployment', 'Unemp_White', 'Unemp_Black', 'Unemp_Hispanic', 'Unemp_Asian']

plt.plot(data.index, data, lw=1.3)
plt.title('Unemployment by Race')
plt.ylabel('Percentage')
plt.xlabel('Year')
plt.legend(data.columns)
plt.grid()
plt.show()