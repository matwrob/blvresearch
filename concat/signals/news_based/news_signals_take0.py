"""
OVERVIEW:
Simple strategy based on news.

First identifies important events by considering alpha and existence of
relevant news on a given day.
Alpha needs to exceed mean by 1 sigma in absolute terms.

Next for each of these days, it checks:
(1) what was the return on that day & invest accordingly

"""
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from concat_overlord.standard import MeanSigma


FIRST_LOC = 0  # span of data used, here from the beginning till the day
LAST_LOC = -1  # before the last day


def get_signals(data):
    days_to_check = _get_days_to_check(data)
    result = pd.Series(index=data.index)
    for date in days_to_check.index:
        result[date] = _get_type_of_signal(date, data)
    return remove_consecutive_values(result)


def _get_candidates_for_signals(data):
    ms = MeanSigma(data['alpha'])
    result = pd.Series(index=data.index)
    for date in data.index[FIRST_LOC:LAST_LOC]:
        yesterday, today, tomorrow = _get_rows(date, data)
        if (_has_relevant_news(today) and
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


def _get_type_of_signal(date, data):
    if _is_negative_suprise(data, date):
        return False
    elif _is_positive_suprise(data, date):
        return True


def _is_negative_suprise(df, date):
    ret = df['alpha']
    if ret[date] < 0:
        return True
    return False


def _is_positive_suprise(df, date):
    ret = df['alpha']
    if ret[date] > 0:
        return True
    return False
