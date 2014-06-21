"""
OVERVIEW:
Simple strategy based on news. First identifies important events by considering
number of news published on a given day, as well as return.
Next it checks the market reaction to those events short after the event
(e.g. 3 trading days) and goes long if this return was significantly positive
or short if it was significantly negative

"""
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from concat_overlord.standard import MeanSigma
from memnews.core import NewsList


def get(data, entity_id):
    result = pd.Series(index=data.index)
    days_to_check = _get_days_to_check(data, entity_id)
    for i, day in enumerate(days_to_check.index):
        if _is_positive_suprise(data, day):
            result[day] = True
        elif _is_negative_suprise(data, day):
            result[day] = False
    return remove_consecutive_values(result)


def _get_days_to_check(data):
    imp = data['important_day']
    ms = MeanSigma(df['alpha'])
    result = pd.Series(index=data.index)
    for date in imp[imp == True].index:
        next_date = imp.index[imp.index.get_loc(date) + 1]
        if (_has_relevant_news(row['news'], entity_id) and
            abs(row['alpha']) > ms.mean + ms.sigma):
            result[date] = True
    return result.dropna()


def _has_relevant_news(news_list, entity_id):
    if isinstance(news_list, list):
        return [n for n in news_list if n['irrelevant'] == False]


def _is_negative_suprise(df, date):
    ret = df['alpha']
    loc = df.index.get_loc(date)
    if (ret[date] < 0 and
        ret[loc:loc + 3].sum() < 0 and
        ret[loc:loc + 3].map(lambda x: -1 if x < 0 else 1).sum() < 0):
        return True
    return False


def _is_positive_suprise(df, date):
    ret = df['alpha']
    loc = df.index.get_loc(date)
    if (ret[date] > 0 and
        ret[loc:loc + 3].sum() > 0 and
        ret[loc:loc + 3].map(lambda x: -1 if x < 0 else 1).sum() > 0):
        return True
    return False
