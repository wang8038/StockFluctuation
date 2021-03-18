import numpy as np
import pandas as pd

def Distribution(s):
	index_name = ['Sum', 'Freq', 'Avg']
	if len(s) < 100:
		return pd.Series(np.nan, index=index_name)
	total = s.sum()
	avg = s.mean()
	freq = len(s)
	return pd.Series([total, freq, avg], index=index_name)