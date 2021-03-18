# The overall distribution characteristics of active commission
import pandas as pd
from Feature_Framework.Utils import Distribution

def General_Distribution(active):
	active = active.copy()
	bids = active.loc[active['ActiveSide'] == 'Bid', 'TradeQty']
	offers = active.loc[active['ActiveSide'] == 'Offer', 'TradeQty']
	bid_stat = Distribution(bids)
	offer_stat = Distribution(offers)
	stat = pd.concat([bid_stat, offer_stat], keys=['ActBid', 'ActOffer'])
	return stat


