# Features time series forecasting
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import rqdatac as rq
rq.init('ricequant', '8ricequant8', ('10.29.135.119', 16010))

def Data_Prepare(files, path, col, timestamp=6):
	X = []
	Inds = []
	for file in files:
		data = pd.read_csv(path + file, header=[0, 1], index_col=0)
		data.dropna(inplace=True)
		factor = data[col].copy()
		factor = (factor - factor.rolling(30).mean()) / factor.rolling(30).std()
		factor.dropna(inplace=True)
		stock = file[:6]
		for i in np.arange(timestamp, len(factor)+1):
			X.append(factor[i-timestamp:i].values)
			Inds.append((stock, factor.index[i-1]))
	X = pd.DataFrame(X)
	X.columns = ['t'+str(c) for c in X.columns]
	X['Ind'] = Inds
	X['stock'] = X['Ind'].map(lambda x:x[0])
	X['date'] = X['Ind'].map(lambda x:x[1])
	X.drop(['Ind'], axis=1, inplace=True)
	return X


path = os.getcwd() + "\\Feature_Framework\\Data\\"
os.chdir(path)
files = sorted(os.listdir())
factors = [('ActBid', 'Sum'), ('ActBid', 'Freq'), ('ActBid', 'Avg'), ('ActOffer', 'Sum'), ('ActOffer', 'Freq'),
		   ('ActOffer', 'Avg'),  ('ActBid', 'LowerSum'), ('ActBid', 'LowerFreq'), ('ActBid', 'LowerAvg'),
		   ('ActBid', 'UpperSum'), ('ActBid', 'UpperFreq'), ('ActBid', 'UpperAvg'), ('ActOffer', 'LowerSum'),
		   ('ActOffer', 'LowerFreq'), ('ActOffer', 'LowerAvg'), ('ActOffer', 'UpperSum'), ('ActOffer', 'UpperFreq'),
		   ('ActOffer', 'UpperAvg'), ('ActBid', 'DecreaseSum'), ('ActBid', 'DecreaseFreq'), ('ActBid', 'DecreaseAvg'),
		   ('ActBid', 'IncreaseSum'), ('ActBid', 'IncreaseFreq'), ('ActBid', 'IncreaseAvg'), ('ActOffer', 'DecreaseSum'),
		   ('ActOffer', 'DecreaseFreq'),('ActOffer', 'DecreaseAvg'),('ActOffer', 'IncreaseSum'),('ActOffer', 'IncreaseFreq'),
		   ('ActOffer', 'IncreaseAvg')]

Result = pd.DataFrame()
for col in factors:
	data = Data_Prepare(files, path, col, timestamp=6)
	data['month'] = data['date'] // 100
	data = data.loc[data['month'] >= 201703].copy()
	months = sorted(data['month'].unique().tolist())
	zz800s = rq.index_components('000906.XSHG', market='cn')
	instrument = rq.instruments(zz800s,market='cn')
	StockList = sorted([i.order_book_id for i in instrument if (i.listed_date <= '2016-01-01') and
						(i.de_listed_date=='0000-00-00')])
	changes = rq.get_price(StockList, '20170101', '20201231', fields=['open', 'close'], expect_df=True)
	changes = np.log(changes['close']+1) - np.log(changes['open']+1)
	changes = changes.reset_index()
	changes.columns = ['stock', 'date', 'change']
	changes['stock'] = changes['stock'].map(lambda x: x[:6])
	changes['date'] = changes['date'].map(lambda x: int(pd.to_datetime(x).strftime('%Y%m%d')))
	data = data.merge(changes, left_on=['stock', 'date'], right_on=['stock', 'date'])
	# Parameters: training period, the previous 6 months
	train_length = 6
	# Parameters: test period, the next 6 months
	test_length = 6
	for i in np.arange(train_length-1, len(months)-test_length):
		train = data.loc[(data.month <= months[i]) & (data.month >= months[i-train_length+1])].copy()
		test = data.loc[(data.month > months[i]) & (data.month <= months[i+test_length])].copy()
		lr = LinearRegression(fit_intercept=False)
		lr.fit(train[['t0', 't1', 't2', 't3', 't4']], train['t5'])
		test['pred'] = lr.predict(test[['t0', 't1', 't2', 't3', 't4']])
		test['pos'] = np.where(test['pred'] > 0, 1, -1)
		test['profit'] = test['pos'] * test['change']
		prediction = test[['stock', 'date', 'pos', 'change', 'profit']].copy()
		prediction['pred_month'] = months[i]
		prediction['factor'] = col[0] + '_' + col[1]
		Result = Result.append(prediction, ignore_index=True)
	print("factor {} runs successfully!".format(col))

# Comprehensive based on each characteristic or feature positions
position = Result.groupby(['pred_month', 'date', 'stock'], as_index=False).agg({'pos': np.mean, 'change': np.mean})
# final position
position['position'] = np.where(position['pos'] > 0, 1, 0)
# The final daily income statistics of individual stocks
position['profit'] = position['position'] * position['change']
# overall annualized return using this Strategy
annual_return = position.groupby('pred_month')['profit'].mean() * 250



