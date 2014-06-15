import pandas as pd


LONG_WINDOW = 30
SHORT_WINDOW = 15


class Position:

    def __init__(self):
        self.invested = False


def get_signals(data):
    l = pd.ewma(data['alpha'], span=LONG_WINDOW)
    s = pd.ewma(data['alpha'], span=SHORT_WINDOW)
    s_above_l = s > l
    return _something(s_above_l)


def _something(series):
    df = pd.DataFrame(series, columns=['s>l'])
    df['block'] = (df['s>l'].shift(1) != df['s>l']).astype(int).cumsum()
    result = pd.Series('', index=series.index)
    for k, v in df.groupby('block'):
        if len(v) > 2:
            result[v.index[2]] = "B" if v['s>l'][0] else "S"
    return result
