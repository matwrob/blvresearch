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


DAYS_AFTER = 2
FIRST_LOC = 0
LAST_LOC = -DAYS_AFTER


def get_news3days_signals(days_to_check, data, first_loc, last_loc):
    first_day = data.index[first_loc + FIRST_LOC]
    last_day = data.index[last_loc + LAST_LOC]
    result = pd.Series(index=data.index)
    for date in days_to_check[first_day:last_day].index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + DAYS_AFTER]
        if _is_negative_suprise(data, date):
            result[signal_day] = False
        elif _is_positive_suprise(data, date):
            result[signal_day] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(data, date):
    loc = data.index.get_loc(date)
    if (data['alpha'][date] < 0 and
        data['alpha'][loc:loc + 1 + DAYS_AFTER].sum() < 0):
        return True
    return False


def _is_positive_suprise(data, date):
    loc = data.index.get_loc(date)
    if (data['alpha'][date] > 0 and
        data['alpha'][loc:loc + 1 + DAYS_AFTER].sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1


DESCRIPTION_BUY = """
This is a BUY signal generated using company news and its stock return.\n
3 days before the signal day relevant news about this company was published
and its stock experienced an abnormal positive alpha.
In addition the cumulative alpha over the following 3 days (including
this day) was also positive and at least 2 out of these 3 days had positive
alpha.
"""

DESCRIPTION_SELL = """
This is a SELL signal generated using company news and its stock return.\n
3 days before the signal day relevant news about this company was published
and its stock experienced an abnoraml negative alpha.
In addition the cumulative alpha over the following 3 days (including
this day) was also negative and at least 2 out of these 3 days had negative
alpha.
"""


def get_news3days_descr(signal):
    if signal == True:
        return DESCRIPTION_BUY
    elif signal == False:
        return DESCRIPTION_SELL
