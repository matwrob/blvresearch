import pandas as pd


def get_return_correlations(entity_id, data, window=33):
    abs_ret = {k: v['abs_ret'] for k, v in data.items()}
    abs_ret = pd.DataFrame(abs_ret)
    result = pd.rolling_corr(abs_ret[entity_id], abs_ret, window=window)
    return result

