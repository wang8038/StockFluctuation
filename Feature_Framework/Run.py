import os
import pandas as pd
import rqdatac as rq
from arctic import Arctic
from Feature_Framework.ActTrades_Process import Active_Trades
from Feature_Framework.General_Distribution import General_Distribution
from Feature_Framework.Pricely_Distribution import Pricely_Distribution
from Feature_Framework.Trend_Distribution import Trend_Distribution

rq.init('ricequant', '8ricequant8', ('10.29.135.119', 16010))
store = Arctic('10.25.24.184')

def Run(stock):
	price = rq.get_price(rq.id_convert(stock), '2017-01-01', '2020-12-31', skip_suspended=True)
	dates = sorted([pd.to_datetime(d).strftime('%Y%m%d') for d in price.index.values])
	result = {}
	for date in dates:
		try:
			active = Active_Trades(stock, date)
			stat1 = General_Distribution(active)
			stat2 = Pricely_Distribution(active)
			stat3 = Trend_Distribution(active)
			result[date] = pd.concat([stat1, stat2, stat3])
		except:
			continue
	data = pd.DataFrame.from_dict(result ,orient='index')
	data.index. name ='date'
	file_path = os.getcwd()
	data.to_csv(file_path + '\\Data\\{}_Statistics.csv'.format(stock))
	print("Stock: {} runs successfully ".format(stock))
	return


if __name__ == '__main__':
	zz800s = rq.index_components('000906.XSHG', market='cn')
	instrument = rq.instruments(zz800s, market='cn')
	StockList = sorted(
		[i.order_book_id[:6] for i in instrument
		 if (i.listed_date <= '2016-01-01') and (i.de_listed_date == '0000-00-00')])
	import multiprocessing
	pool = multiprocessing.Pool(processes=5)
	for stock in StockList:
		pool.apply_async(Run, (stock,))
	pool.close()
	pool.join()