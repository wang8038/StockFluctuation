# Distribution characteristics of active orders based on intraday trends
import numpy as np
import pandas as pd
from Feature_Framework.Utils import Distribution

def Trend_Distribution(active):
	active = active.copy()
	bids = active.loc[active['ActiveSide'] == 'Bid'].copy()
	bids['PriceAvg'] = bids['Price'].rolling(200, min_periods=1, center=False).mean()
	bids['lvl'] = np.where(bids['Price'] > bids['PriceAvg'], 'Increase', 'Decrease')
	bid_stat = bids['TradeQty'].groupby(bids['lvl']).apply(func=lambda x: Distribution(x.values))
	bid_stat.index = [i[0] + i[1] for i in bid_stat.index]
	offers = active.loc[active['ActiveSide'] == 'Offer'].copy()
	offers['PriceAvg'] = offers['Price'].rolling(200, min_periods=1, center=False).mean()
	offers['lvl'] = np.where(offers['Price'] > offers['PriceAvg'], 'Increase', 'Decrease')
	offer_stat = offers['TradeQty'].groupby(offers['lvl']).apply(func=lambda x: Distribution(x.values))
	offer_stat.index = [i[0] + i[1] for i in offer_stat.index]
	stat = pd.concat([bid_stat, offer_stat], keys=['ActBid', 'ActOffer'])
	return stat


