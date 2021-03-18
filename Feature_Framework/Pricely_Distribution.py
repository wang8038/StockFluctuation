# Distribution characteristics of active commissions based on high and low prices
import numpy as np
import pandas as pd
from Feature_Framework.Utils import Distribution

def Pricely_Distribution(active):
	active = active.copy()
	bids = active.loc[active['ActiveSide'] == 'Bid'].copy()
	bid_price_median = np.median(bids['Price'].unique())
	bids_below = bids.loc[bids.Price <= bid_price_median, 'TradeQty'].values
	bids_up = bids.loc[bids.Price > bid_price_median, 'TradeQty'].values
	bid_stat = pd.concat([Distribution(bids_below), Distribution(bids_up)], keys=['Lower', 'Upper'])
	bid_stat.index = [i[0] + i[1] for i in bid_stat.index]
	offers = active.loc[active['ActiveSide'] == 'Offer'].copy()
	offer_price_median = np.median(offers['Price'].unique())
	offers_below = offers.loc[offers.Price <= offer_price_median, 'TradeQty'].values
	offers_up = offers.loc[offers.Price > offer_price_median, 'TradeQty'].values
	offer_stat = pd.concat([Distribution(offers_below), Distribution(offers_up)], keys=['Lower', 'Upper'])
	offer_stat.index = [i[0] + i[1] for i in offer_stat.index]
	stat = pd.concat([bid_stat, offer_stat], keys=['ActBid', 'ActOffer'])
	return stat

