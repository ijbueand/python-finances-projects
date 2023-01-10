import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import yfinance as yfin
import matplotlib.pyplot as plt
from scipy.stats import norm 

yfin.pdr_override()

# This code calculates the value at risk (VaR) of a portfolio of stocks.

tickers = ['TEF.MC', 'IBE.MC', 'SGRE.MC', 'MAP.MC']
weights = np.array([0.5, 0.2, 0.2, 0.1])

data = pd.DataFrame()

for t in tickers:
    data[t] = wb.get_data_yahoo(t, start='2013-01-01')['Adj Close']

''' Calculate the simple returns for each stock by dividing the 
closing price for one day by the previous day's closing price. '''

returns = data.pct_change() 

''' Calculate the covariance matrix of the returns, which is a 
measure of how the returns of the different stocks are related. '''

cov_matrix = returns.cov()

''' Using the weights and the mean returns, we calculate the 
mean return of the portfolio. It also calculates the standard 
deviation of the portfolio's returns, which is a measure of the portfolio's risk.'''

returns_mean = returns.mean()
portfolio_mean = returns_mean.dot(weights)
portfolio_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))

''' Then define an investment amount and calculate the expected value 
and standard deviation of the investment. Also define a confidence 
level and use the normal distribution to calculate the value at risk 
(VaR) of the investment. '''

investment = float(150000)
mean_investment = (1+portfolio_mean)*investment
stdev_investment = investment * portfolio_stdev

conf_level = 0.05
cut = norm.ppf(conf_level, mean_investment, stdev_investment)
var_id = investment - cut
num_days = int(100)

var_array = []

''' Finally, calculate the VaR of the investment for a number of days 
in the future and plot the results. The VaR of the investment is an 
estimate of the maximum loss that the investment is expected to incur 
over a given time period with a certain level of confidence. '''

print('\nThe maximum loss of your portfolio with ' + str(investment) + '€\nwith a confidence level of ' + str((1-conf_level)*100) + '% and for the following ' + str(num_days) + ' days is:\n')

for i in range(1, num_days):
    var_array.append(np.round(var_id*np.sqrt(i), 2))
    print('To ' + str(i) + ' days VaR(' + str((1-conf_level)*100) + '%) = ' + str(np.round(var_id*np.sqrt(i), 2)))

plt.xlabel('Days')
plt.ylabel('Maximum loss of our portfolio')
plt.title('Maximum portfolio loss for the period')
plt.plot(var_array, 'b')
plt.show()