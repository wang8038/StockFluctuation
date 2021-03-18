# Pre-processing of transaction details and extracting active entrusted data
import numpy as np
from arctic import Arctic
store = Arctic('10.25.24.184')


def last(s): return s.iloc[-1]


def first(s): return s.iloc[0]


def Active_Trades(stock, date):
	trade = store['trade_s.' + stock].read(date).data
	if stock[0] == '6':
		trade['Time'] = trade['TradeTime'] - trade['TradeDate'] * 1000000
		EndTime = 145700 if date >= '20180820' else 150000
		trade = trade.loc[(trade['Time'] >= 93000) & (trade['Time'] < EndTime)]
	else:
		trade = trade.loc[trade.ExecType == 'F'].copy()
		trade['TradeAmt'] = trade['Price'] * trade['TradeQty']
		trade['Time'] = trade['TradeTime'] - trade['TradeDate'] * 1000000000
		trade = trade.loc[(trade['Time'] >= 93000000) & (trade['Time'] < 145700000)]
	trade['ActiveAppl'] = np.where(trade['BidApplSeqNum'] > trade['OfferApplSeqNum'], trade['BidApplSeqNum'],
								   trade['OfferApplSeqNum'])
	trade['ActiveSide'] = np.where(trade['BidApplSeqNum'] > trade['OfferApplSeqNum'], 'Bid', 'Offer')
	active = trade.groupby(['ActiveAppl', 'ActiveSide'], as_index=False).agg({'TradeQty': np.sum, 'TradeAmt': np.sum,
																			  'Price': last, 'Time': first})
	return active

