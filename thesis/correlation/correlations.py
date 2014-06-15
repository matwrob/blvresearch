import pandas as pd


def get_return_correlations(entity_id, data):
	result = {k: v['abs_ret'] for k, v in data.items()}
	result = pd.DataFrame(result)
	
