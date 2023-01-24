'''Este programa dice si las empresas que conforman el S&P500 (una por una)
están por encima o por debajo de la media movil de 200 periodos. Esta es una
media movil lenta, de forma que si está por encima está en una tendencia alcista
y si está por debajo está en una tendencia bajista.'''

import yahoo_fin.stock_info as si
import yfinance as yf

tickersA = []
tickersB = []

lt = si.tickers_sp500()

for m in range(len(lt)):
    df = yf.download(lt[m], '2018-01-01', progress=False)['Close']
    if float(df[-1:]) > float(df[-200:].mean()):
        tickersA.append(lt[m])
    else:
        tickersB.append(lt[m])
        
print("Number of periods: ", len(df))
print("\n")
print("Above average: ", tickersA)
print("\n")
print("Below average: ", tickersB)
