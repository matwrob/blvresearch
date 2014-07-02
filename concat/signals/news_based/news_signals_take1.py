"""
OVERVIEW:
Simple strategy based on news.

First identifies important events by considering alpha and existence of
relevant news on a given day.
Alpha needs to exceed mean by 1 sigma in absolute terms.

Next for each of these days, it checks:
(1) what was the return on that day
(2) what was the return over the next 3 days
(3) how many down days in comparison to how many up days occurred in the next
    3 days

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.utils import remove_consecutive_values


FIRST_LOC = 0
LAST_LOC = -3


def get_signals(data):
    days_to_check = get_days_to_check(data, FIRST_LOC, LAST_LOC)
    result = pd.Series(index=data.index)
    for date in days_to_check.index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + 3]
        if _is_negative_suprise(data, date):
            result[signal_day] = False
        elif _is_positive_suprise(data, date):
            result[signal_day] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(df, date):
    loc = df.index.get_loc(date)
    if (df['alpha'][date] < 0 and
        df['alpha'][loc:loc + 3].sum() < 0 and
        df['alpha'][loc:loc + 3].map(func).sum() < 0):
        return True
    return False


def _is_positive_suprise(df, date):
    loc = df.index.get_loc(date)
    if (df['alpha'][date] > 0 and
        df['alpha'][loc:loc + 3].sum() > 0 and
        df['alpha'][loc:loc + 3].map(func).sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1
