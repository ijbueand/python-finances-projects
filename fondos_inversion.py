import investpy
import time 
import pandas as pd
import matplotlib.pyplot as plt
import quantstats as qs
import ffn

# Curación de activos de fondos

tickers = investpy.funds.get_funds()[['country', 'name', 'symbol']]
tickers = tickers[tickers['country'] == 'spain']

bestinver = list(tickers['name'][tickers['name'].str.contains('Bestinver', case = False)])
azvalor = list(tickers['name'][tickers['name'].str.contains('Azvalor', case = False)])
magallanes = list(tickers['name'][tickers['name'].str.contains('Magallanes', case = False)])
cobas = list(tickers['name'][tickers['name'].str.contains('Cobas', case = False)])
baelo = list(tickers['name'][tickers['name'].str.contains('Baelo', case = False)])
numantia = list(tickers['name'][tickers['name'].str.contains('Numantia', case = False)])
gpm = list(tickers['name'][tickers['name'].str.contains('GPM', case = False)])

fondos_spain = bestinver + azvalor + magallanes + cobas + baelo + numantia + gpm 

# Descarga de datos

df = pd.DataFrame()
for i in range(len(fondos_spain)):
    time.sleep(3)
    df[i] = investpy.funds.get_fund_historical_data(fund = fondos_spain[i], country = 'spain', from_date ='01/01/2017', to_date = '01/01/2022')['Close']
    df

df.columns = fondos_spain

df = df.interpolate()

bestinver = df.loc[:, df.columns.isin(bestinver)]
azvalor = df.loc[:, df.columns.isin(azvalor)]
magallanes = df.loc[:, df.columns.isin(magallanes)]
cobas = df.loc[:, df.columns.isin(cobas)]
baelo = df.loc[:, df.columns.isin(baelo)]
numantia = df.loc[:, df.columns.isin(numantia)]
gpm = df.loc[:, df.columns.isin(gpm)]

# Utilizando FFN

stats = df[['Azvalor Internacional Fi', 'Esfera I Baelo Patrimonio Fi', 'Renta 4 Multigestión Numantia Patrimonio Global Fi']].calc_stats()
stats.display()

stats_total = pd.DataFrame(df.calc_stats().stats.T).reset_index()
stats_total.columns

# Análisis haciendo filtros
stats_total['index'][stats_total['max_drawdown'] <= -0.3]
stats_total['index'][stats_total['avg_drawdown'] <= -0.1]
stats_total['index'][stats_total['calmar'] >= 0.5]
stats_total['index'][stats_total['yearly_sortino'] >= 3]

# Análisis utilizando quantstats
qs.reports.html(numantia['Renta 4 Multigestión Numantia Patrimonio Global Fi'], 'SPY', output = 'numantia.html')
