"""
OVERVIEW:
First identifies important events, i.e.
(1) relevant news need to exist
(2) alpha needs to exceed expected alpha by 1 standard deviation

    Remark: alpha moments are calculated based on previous 6 months

Next for each of these days, it checks:
(3) what was the return on that day
(4) what was the return over the following 3 days
(5) how many down days in comparison to how many up days occurred
    over the following 3 days

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


DAYS_AFTER = 3
FIRST_LOC = 0
LAST_LOC = -DAYS_AFTER


def get_signals(data):
    days_to_check = get_days_to_check(data, FIRST_LOC, LAST_LOC)
    result = pd.Series(index=data.index)
    for date in days_to_check.index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + DAYS_AFTER]
        if _is_negative_suprise(data, date):
            result[signal_day] = False
        elif _is_positive_suprise(data, date):
            result[signal_day] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(df, date):
    loc = df.index.get_loc(date)
    if (df['alpha'][date] < 0 and
        df['alpha'][loc + 1:loc + 1 + DAYS_AFTER].sum() < 0 and
        df['alpha'][loc + 1:loc + 1 + DAYS_AFTER].map(func).sum() < 0):
        return True
    return False


def _is_positive_suprise(df, date):
    loc = df.index.get_loc(date)
    if (df['alpha'][date] > 0 and
        df['alpha'][loc + 1:loc + 1 + DAYS_AFTER].sum() > 0 and
        df['alpha'][loc + 1:loc + 1 + DAYS_AFTER].map(func).sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1
