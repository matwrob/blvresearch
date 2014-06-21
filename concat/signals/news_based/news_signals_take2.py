"""
OVERVIEW:
Simple strategy based on news.

First identifies important events by considering alpha and existence of
relevant news on a given day.
Alpha needs to exceed mean by 1 sigma in absolute terms.

Next for each of these days, it checks:
(1) what was the return on that day
(2) what was the return over next 3 days
(3) how many down days in comparison to how many up days occurred in the next
    3 days
(4) is price close to 2 month low (for sell signal) or 2 month high (for buy
    signal) level?

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from concat_overlord.standard import MeanSigma
from memnews.core import NewsList


TODAY = dt.datetime.today()
TODAY = pd.Timestamp(TODAY, tz='UTC')

MARGIN = 3

def get_signals(data):
    days_to_check = _get_days_to_check(data)
    result = pd.Series(index=data.index)
    for date in days_to_check.index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + 3]
        result[signal_day] = _get_type_of_signal(date, data)
    return remove_consecutive_values(result)


def _get_days_to_check(data):
    ms = MeanSigma(data['alpha'])
    result = pd.Series(index=data.index)
    for date, row in data[:-MARGIN].iterrows():
        loc = data.index.get_loc(date)
        next_date = data.index[loc + 1]
        next_row = data.loc[next_date]
        cond1 = _has_relevant_news(row['news'])
        cond2 = abs(row['alpha']) > ms.mean + ms.sigma
        cond3 = abs(next_row['alpha']) > ms.mean + ms.sigma
        if cond1 and (cond2 or cond3):
            result[date] = True
    return result.dropna()


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
    loc = df.index.get_loc(date)
    if (ret[date] < 0 and
        ret[loc:loc + 3].sum() < 0 and
        ret[loc:loc + 3].map(func).sum() < 0 and
        # ret[loc-5:loc].map(func).sum() <= -1 and
        ret[loc-5:loc].sum() < 0):
        return True
    return False


def _is_positive_suprise(df, date):
    ret = df['alpha']
    loc = df.index.get_loc(date)
    if (ret[date] > 0 and
        ret[loc:loc + 3].sum() > 0 and
        ret[loc:loc + 3].map(func).sum() > 0 and
        # ret[loc-5:loc].map(func).sum() >= 1 and
        ret[loc-5:loc].sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1
