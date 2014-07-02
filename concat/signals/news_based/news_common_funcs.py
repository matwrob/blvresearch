import pandas as pd

from concat_overlord.standard import MeanSigma


def get_days_to_check(data, first_loc, last_loc):
    ms = MeanSigma(data['alpha'])
    result = pd.Series(index=data.index)
    for date in data.index[first_loc:last_loc]:
        yesterday, today, tomorrow = _get_rows(date, data)
        if (_has_relevant_news(today['news']) and
            (abs(yesterday['alpha']) > ms.mean + ms.sigma or
             abs(today['alpha']) > ms.mean + ms.sigma or
             abs(tomorrow['alpha']) > ms.mean + ms.sigma)):
            result[date] = True
    return result.dropna()


def _get_rows(date, data):
    loc = data.index.get_loc(date)
    row1 = data.loc[data.index[loc - 1]]
    row2 = data.loc[data.index[loc]]
    row3 = data.loc[data.index[loc + 1]]
    return row1, row2, row3


def _has_relevant_news(news_list):
    if isinstance(news_list, list):
        return [n for n in news_list if n['irrelevant'] == False]
