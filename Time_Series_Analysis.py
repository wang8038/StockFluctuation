# Characteristic time series attribute test
import os
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.stats.diagnostic import acorr_ljungbox


def Time_Series_Analysis(s):
	pacfs = pacf(s, nlags=5)[1:].tolist()
	acfs = acf(s, nlags=5)[1:].tolist()
	adf = ADF(s)[1]
	white_noise = acorr_ljungbox(s, lags=10)[1][0]
	ts = pacfs + acfs + [adf, white_noise]
	ts = pd.Series(ts, index=['pacf1','pacf2','pacf3','pacf4','pacf5','acf1','acf2','acf3','acf4','acf5',
							  'adf','white_noise'])
	return ts


path = os.getcwd() + "/Feature_Framework/Data/"
os.chdir(path)
files = sorted(os.listdir())
result = {}
for file in files:
	data = pd.read_csv(path + file,header=[0,1],index_col=0)
	data.dropna(inplace=True)
	r = {}
	for col in data.columns:
		r[col] = Time_Series_Analysis(data[col])
	r = pd.DataFrame.from_dict(r, orient='index')
	stock = file[:6]
	result[stock] = r
result = pd.concat(result, axis=0)
result = result.reset_index()
result_mean = result.groupby(['level_1','level_2']).mean()
# Characteristic time series attributes
print(result_mean.describe())


